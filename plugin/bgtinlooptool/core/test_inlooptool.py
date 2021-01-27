# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 13:04:52 2020

@author: chris.kerklaan

Tests are used for single/unit testing and integrated testing
"""

# System imports
import os
import sys

# Third-party imports
import ogr
import unittest

# Globals

__file__ = sys.argv[0]

DATA_PATH = os.path.join(os.path.dirname(__file__), "../test-data")
SURFACES_INPUT_FILENAME = os.path.join(DATA_PATH, 'extract.zip')
PIPES_INPUT_FILENAME = os.path.join(DATA_PATH, 'getGeoPackage_1134.gpkg')
BUILDINGS_INPUT_FILENAME = os.path.join(DATA_PATH, 'bag.gpkg')
# Find package
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.append(os.path.dirname(__file__))

# Local/test imports
from .inlooptool import *
from core.constants import *


# Drivers

class UnitDatabase(unittest.TestCase):
    """ used for both unittests and integrated testing"""

    def empty_result_table(self):
        """Can the Database succesfully generate an empty result table?"""
        self.db = Database()
        out_gpkg_fn = os.path.join(DATA_PATH, 'empty_result.gpkg')
        if os.path.exists(out_gpkg_fn):
            os.remove(out_gpkg_fn)
        hard_gpkg_ds = GPKG_DRIVER.CreateDataSource(out_gpkg_fn)
        src_lyr = self.db.result_table
        hard_gpkg_ds.CopyLayer(src_lyr, RESULT_TABLE_NAME)
        hard_gpkg_ds = None
        result = ogr.Open(out_gpkg_fn)
        self.assertTrue(isinstance(result, ogr.DataSource), 'empty_result.gpkg is not a valid ogr.Datasource')

    def test_import_surfaces(self):
        """ Test _database loading using different assert"""
        self.db = Database()

        """ Tests if the surfaces have a ogr layer loaded into the memory db"""
        self.db.import_surfaces_raw(SURFACES_INPUT_FILENAME)

        checks = []
        for surface_type in ALL_USED_SURFACE_TYPES:
            layer = self.db.mem_database.GetLayerByName(surface_type)
            if layer is not None:
                checks.append(True)
        self.assertTrue(
            len(checks) == len(ALL_USED_SURFACE_TYPES),
            "not all layers are loaded into the memory db"
        )

        """ Tests if all loaded surfaces are a polygon"""
        self.db.clean_surfaces()

        for surface_type in ALL_USED_SURFACE_TYPES:
            layer = self.db.mem_database.GetLayerByName(surface_type)
            for feature in layer:
                geom = feature.geometry()
                geom_type = geom.GetGeometryType()
                self.assertTrue(
                    geom_type == ogr.wkbPolygon,
                    "geometry in layer {} is not a polygon".format(surface_type)
                )

    def test_classify(self):
        params = InputParameters()
        it = BGTInloopTool(params)
        db = it._database
        it.import_surfaces(SURFACES_INPUT_FILENAME)

        self.assertTrue(db.bgt_surfaces is not None,
                        "db.bgt_surfaces is None")

        parameters = InputParameters()
        db.classify_surfaces(parameters)

        """ Tests if all features are classified"""
        for feature in db.bgt_surfaces:
            self.assertTrue(feature['type_verharding'] is not None,
                            "type verharding is None")

    def test_import_pipes(self):
        params = InputParameters()
        it = BGTInloopTool(params)
        db = it._database
        it.import_pipes(file_path=PIPES_INPUT_FILENAME)
        self.assertTrue(db.pipes.GetFeatureCount() == 8986)

    def test_calculate_runoff_targets(self):
        parameters = InputParameters()
        it = BGTInloopTool(parameters)
        it.import_surfaces(file_path=SURFACES_INPUT_FILENAME)
        it.import_pipes(file_path=PIPES_INPUT_FILENAME)

        # speed test
        it.calculate_distances(parameters)  # 7 minutes 30 secs

        distances = it._database.mem_database.GetLayerByName('pipe_distances')

        # Features are only added to this layer, if it countains a distance
        # If features all fall out the search range, then this will give a error
        self.assertTrue(distances.GetFeatureCount() > 0,
                        """Features are only added to this layer, if it countains a distance
                            If features all fall out the search range, then this will give a error
                            """)

        distances = it._database.mem_database.GetLayerByName('water_distances')

        # Features are only added to this layer, if it countains a distance
        # If features all fall out the search range, then this will give a error
        self.assertTrue(distances.GetFeatureCount() > 0,
                        """Features are only added to this water distance layer, if it countains a distance
                            If features all fall out the search range, then this will give a error
                            """)

        it.calculate_distances(parameters, use_index=False)  # 16minutes and 2 seconds

        distances = it._database.mem_database.GetLayerByName('pipe_distances')

        # Features are only added to this layer, if it countains a distance
        # If features all fall out the search range, then this will give a error
        self.assertTrue(distances.GetFeatureCount() > 0,
                        """Features are only added to this layer, if it countains a distance
                            If features all fall out the search range, then this will give a error
                            """)

        distances = it._database.mem_database.GetLayerByName('water_distances')

        # Features are only added to this layer, if it countains a distance
        # If features all fall out the search range, then this will give a error
        self.assertTrue(distances.GetFeatureCount() > 0,
                        """Features are only added to this water distance layer, if it countains a distance
                            If features all fall out the search range, then this will give a error
                            """)

        it.calculate_runoff_targets()
        out_gpkg_fn = os.path.join(DATA_PATH, 'calculated_result.gpkg')
        if os.path.exists(out_gpkg_fn):
            os.remove(out_gpkg_fn)
        hard_gpkg_ds = GPKG_DRIVER.CreateDataSource(out_gpkg_fn)
        src_lyr = it._database.result_table
        hard_gpkg_ds.CopyLayer(src_lyr, RESULT_TABLE_NAME)
        hard_gpkg_ds = None
        result = ogr.Open(out_gpkg_fn)
        self.assertTrue(isinstance(result, ogr.DataSource), 'calculated_result.gpkg is not a valid ogr.Datasource')

    def test_decision_tree(self):
        parameters = InputParameters()
        it = InloopTool(parameters)
        it._database.create_table(table_name=SURFACES_TABLE_NAME, table_schema=SURFACES_TABLE_SCHEMA)
        surfaces_layer = it._database.mem_database.GetLayerByName(SURFACES_TABLE_NAME)
        surface = ogr.Feature(surfaces_layer.GetLayerDefn())

        def reset_surface():
            for distance in ['distance_gemengd_riool', 'distance_hemelwaterriool', 'distance_vuilwaterriool',
                             'distance_infiltratievoorziening', 'distance_oppervlaktewater']:
                surface[distance] = 9999

        template_test_result = {
            'gemengd_riool': 0,
            'hemelwaterriool': 0,
            'vgs_hemelwaterriool': 0,
            'infiltratievoorziening': 0,
            'niet_aangesloten': 0
        }

        # Beslisboom voor bouwwerken testen

        # bouwwerk bij water, 
        # niet aangesloten: 100
        reset_surface()
        surface.surface_type = 'pand'
        surface.type_verharding = 'dak'
        surface.distance_oppervlakte_water = 1
        test_result = it.decision_tree(surface, parameters)
        valid_result = template_test_result.copy()
        valid_result['niet_aangesloten'] = 100
        self.assertEquals(test_result, valid_result, 'FOUT voor: Pand bij water')

        # Gemengd plus hwa of infiltratie, nieuw pand, hwa dichtsbij
        # gemengd 50, hwa 50
        reset_surface()
        parameters.afkoppelen_hellende_daken = True
        surface.surface_type = 'pand'
        surface.type_verharding = 'dak'
        surface.build_year = 2014
        surface.distance_gemengd_riool = 2
        surface.distance_hemelwaterriool = 2
        test_result = it.decision_tree(surface, parameters)
        valid_result = template_test_result.copy()
        valid_result['gemengd_riool'] = 50
        valid_result['hemelwaterriool'] = 50
        self.assertEquals(test_result, valid_result, 'FOUT voor: Gemengd plus hwa of infiltratie, nieuw pand, hwa dichtsbij')

        # Gemengd plus hwa of infiltratie, nieuw pand, infiltratie dichtsbij
        # infiltratie 100
        reset_surface()
        parameters.afkoppelen_hellende_daken = True
        surface.surface_type = 'pand'
        surface.type_verharding = 'dak'
        surface.build_year = 2014
        surface.distance_gemengd_riool = 2
        surface.distance_hemelwaterriool = 10
        surface.distance_infiltratievoorziening = 2
        test_result = it.decision_tree(surface, parameters)
        valid_result = template_test_result.copy()
        valid_result['infiltratievoorziening'] = 100
        self.assertEquals(test_result, valid_result, 'FOUT voor: Gemengd plus hwa of infiltratie, infiltratie dichtsbij')

        # Gemengd plus hwa, oud pand
        # gemengd 50, hwa 50
        reset_surface()
        parameters.afkoppelen_hellende_daken = True
        surface.surface_type = 'pand'
        surface.type_verharding = 'dak'
        surface.build_year = 1900
        surface.distance_gemengd_riool = 3
        surface.distance_hemelwaterriool = 3
        test_result = it.decision_tree(surface, parameters)
        valid_result = template_test_result.copy()
        valid_result['gemengd_riool'] = 50
        valid_result['hemelwaterriool'] = 50
        self.assertEquals(test_result, valid_result, 'FOUT voor: Gemengd plus hwa, oud pand ')

        # Gemengd plus hwa of infiltratie, oud pand, maar niet afkoppelen hellende daken
        # Altijd gemengd
        reset_surface()
        parameters.afkoppelen_hellende_daken = False
        surface.surface_type = 'pand'
        surface.type_verharding = 'dak'
        surface.build_year = 1900
        surface.distance_gemengd_riool = 3
        surface.distance_hemelwaterriool = 3
        surface.distance_infiltratievoorziening = 1
        test_result = it.decision_tree(surface, parameters)
        valid_result = template_test_result.copy()
        valid_result['gemengd_riool'] = 100
        self.assertEquals(test_result, valid_result, 'FOUT voor: Gemengd plus hwa of infiltratie, oud pand, maar niet afkoppelen hellende daken ')

        # Alleen gemengd in de buurt
        # 100% gemengd
        reset_surface()
        surface.surface_type = 'pand'
        surface.type_verharding = 'dak'
        surface.distance_gemengd_riool = 1
        it.decision_tree(surface, parameters)
        test_result = it.decision_tree(surface, parameters)
        valid_result = template_test_result.copy()
        valid_result['gemengd_riool'] = 100
        self.assertEquals(test_result, valid_result,
                          'FOUT voor: Alleen gemengd in de buurt')

        # Alleen hemelwaterriool in de buurt
        # 100% hemelwaterriool
        reset_surface()
        surface.surface_type = 'pand'
        surface.type_verharding = 'dak'
        surface.distance_hemelwaterriool = 1
        test_result = it.decision_tree(surface, parameters)
        valid_result = template_test_result.copy()
        valid_result['hemelwaterriool'] = 100
        self.assertEquals(test_result, valid_result,
                          'FOUT voor: Alleen hemelwaterriool in de buurt')

        # Alleen infiltratievoorziening in de buurt
        # 100% infiltratievoorziening
        reset_surface()
        surface.surface_type = 'pand'
        surface.type_verharding = 'dak'
        surface.distance_infiltratievoorziening = 1
        test_result = it.decision_tree(surface, parameters)
        valid_result = template_test_result.copy()
        valid_result['infiltratievoorziening'] = 100
        self.assertEquals(test_result, valid_result,
                          'FOUT voor: Alleen infiltratievoorziening in de buurt')

        # Alleen oppervlaktewater in de buurt
        # 100% niet aangesloten
        reset_surface()
        surface.surface_type = 'pand'
        surface.type_verharding = 'dak'
        surface.distance_oppervlaktewater = 3
        test_result = it.decision_tree(surface, parameters)
        valid_result = template_test_result.copy()
        valid_result['niet_aangesloten'] = 100
        self.assertEquals(test_result, valid_result,
                          'FOUT voor: Alleen oppervlaktewater in de buurt')

        # Wegdeel, gemengd riool
        reset_surface()
        surface.surface_type = 'wegdeel'
        surface.type_verharding = 'verhard'
        surface.distance_gemengd_riool = 1
        test_result = it.decision_tree(surface, parameters)
        valid_result = template_test_result.copy()
        valid_result['gemengd_riool'] = 100
        self.assertEquals(test_result, valid_result,
                          'FOUT voor: Wegdeel')

        # Wegdeel, alleen rwa
        reset_surface()
        surface.surface_type = 'wegdeel'
        surface.type_verharding = 'verhard'
        surface.distance_hemelwaterriool = 1
        test_result = it.decision_tree(surface, parameters)
        valid_result = template_test_result.copy()
        valid_result['hemelwaterriool'] = 100
        self.assertEquals(test_result, valid_result,
                          'FOUT voor: Wegdeel, alleen rwa')

        # Wegdeel, alleen infiltratievoorziening
        reset_surface()
        surface.surface_type = 'wegdeel'
        surface.type_verharding = 'verhard'
        surface.distance_infiltratievoorziening = 1
        test_result = it.decision_tree(surface, parameters)
        valid_result = template_test_result.copy()
        valid_result['infiltratievoorziening'] = 100
        self.assertEquals(test_result, valid_result,
                          'FOUT voor: Wegdeel, alleen infiltratievoorziening')

        # Wegdeel, infiltratievoorziening en hemelwaterriool
        reset_surface()
        surface.surface_type = 'wegdeel'
        surface.type_verharding = 'verhard'
        surface.distance_infiltratievoorziening = 1
        surface.distance_hemelwaterriool = 0.5
        test_result = it.decision_tree(surface, parameters)
        valid_result = template_test_result.copy()
        valid_result['hemelwaterriool'] = 100
        self.assertEquals(test_result, valid_result,
                          'FOUT voor: Wegdeel, infiltratievoorziening en hemelwaterriool')

        # Wegdeel, infiltratie + gemengd + hwa
        reset_surface()
        surface.surface_type = 'wegdeel'
        surface.type_verharding = 'verhard'
        surface.distance_infiltratievoorziening = 2
        surface.distance_hemelwaterriool = 2
        surface.distance_gemengd_riool = 1
        test_result = it.decision_tree(surface, parameters)
        valid_result = template_test_result.copy()
        valid_result['infiltratievoorziening'] = 100
        self.assertEquals(test_result, valid_result,
                          'FOUT voor: Wegdeel, infiltratie + gemengd + hwa')

        # Wegdeel, gemengd + hwa
        reset_surface()
        surface.surface_type = 'wegdeel'
        surface.type_verharding = 'verhard'
        surface.distance_hemelwaterriool = 40
        surface.distance_gemengd_riool = 1
        test_result = it.decision_tree(surface, parameters)
        valid_result = template_test_result.copy()
        valid_result['gemengd_riool'] = 100
        self.assertEquals(test_result, valid_result,
                          'FOUT voor: Wegdeel, gemengd + hwa (HWA op 40m)')

        # Wegdeel, oppervlaktewater
        reset_surface()
        surface.surface_type = 'wegdeel'
        surface.type_verharding = 'verhard'
        surface.distance_oppervlaktewater = 100
        test_result = it.decision_tree(surface, parameters)
        valid_result = template_test_result.copy()
        valid_result['niet_aangesloten'] = 100
        self.assertEquals(test_result, valid_result,
                          'FOUT voor: Wegdeel, oppervlaktewater')

    def test_add_buildings(self):
        parameters = InputParameters()
        it = InloopTool(parameters)
        it.import_surfaces(file_path=SURFACES_INPUT_FILENAME)
        it.import_buildings(file_path=BUILDINGS_INPUT_FILENAME)
        it._database.add_build_year_to_surface()

        for surface in it._database.bgt_surfaces:
            if surface['surface_type'] == 'pand':
                self.AssertTrue(surface['build_year'] is not None,
                                """ surface of type pand does not have a build year"""
                                )


if __name__ == '__main__':
    unittest.main()
