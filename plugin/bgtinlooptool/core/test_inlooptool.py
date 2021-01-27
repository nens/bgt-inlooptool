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
from core.inlooptool import *
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
        it.calculate_distances(parameters) # 7 minutes 30 secs
        
        
        distances = it._database.mem_database.GetLayerByName('pipe_distances')
        
        # Features are only added to this layer, if it countains a distance
        # If features all fall out the search range, then this will give a error
        self.AssertTrue(distances.GetFeatureCount() > 0,
                        """Features are only added to this layer, if it countains a distance
                            If features all fall out the search range, then this will give a error
                            """)
                
        distances = it._database.mem_database.GetLayerByName('water_distances')
        
        # Features are only added to this layer, if it countains a distance
        # If features all fall out the search range, then this will give a error
        self.AssertTrue(distances.GetFeatureCount() > 0,
                        """Features are only added to this water distance layer, if it countains a distance
                            If features all fall out the search range, then this will give a error
                            """)

        
        it.calculate_distances(parameters, use_index=False) # 16minutes and 2 seconds
        
                
        distances = it._database.mem_database.GetLayerByName('pipe_distances')
        
        # Features are only added to this layer, if it countains a distance
        # If features all fall out the search range, then this will give a error
        self.AssertTrue(distances.GetFeatureCount() > 0,
                        """Features are only added to this layer, if it countains a distance
                            If features all fall out the search range, then this will give a error
                            """)
                
        distances = it._database.mem_database.GetLayerByName('water_distances')
        
        # Features are only added to this layer, if it countains a distance
        # If features all fall out the search range, then this will give a error
        self.AssertTrue(distances.GetFeatureCount() > 0,
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
        from core.inlooptool import *
        parameters = InputParameters()
        it = InloopTool(parameters)
        it._database.mem_database = ogr.Open('C:/Users/Emile.deBadts/Documents/Projecten/v0099_bgt_inlooptool/mem_database.gpkg',1)
        surface = it._database.bgt_surfaces.GetFeature(1)
        
        def reset_surface():
            for distance in ['distance_gemengd_riool', 'distance_hemelwaterriool', 'distance_vuilwaterriool',
                             'distance_infiltratievoorziening', 'distance_oppervlaktewater']:
                surface[distance] = 9999
        
        surface.ExportToJson(_)
                
        # Beslisboom voor bouwwerken testen
                
        # bouwwerk bij water, 
        # niet aangesloten: 100
        reset_surface()
        surface.surface_type = 'pand'
        surface.distance_oppervlakte_water = 1
        it.decision_tree(surface, parameters)
        
        # Gemengd plus hwa of infiltratie, nieuw pand, hwa dichtsbij
        # gemengd 50, hwa 50
        reset_surface()
        parameters.afkoppelen_hellende_daken = True
        surface.surface_type = 'pand'
        surface.build_year = 2014
        surface.distance_gemengd_riool = 2
        surface.distance_hemelwaterriool = 2
        it.decision_tree(surface, parameters)
        
        # Gemegnd plus hwa of infiltratie, infiltratie dichtsbij 
        # gemengd 50, infiltratie 50
        reset_surface()
        parameters.afkoppelen_hellende_daken = True
        surface.surface_type = 'pand'
        surface.build_year = 2014
        surface.distance_gemengd_riool = 2
        surface.distance_hemelwaterriool = 10
        surface.distance_infiltratievoorziening = 2
        it.decision_tree(surface, parameters)

        # Gemengd plus hwa of infiltratie, oud pand 
        # Altijd 100 of dichtsbijzijnde
        reset_surface()
        parameters.afkoppelen_hellende_daken = True
        surface.surface_type = 'pand'
        surface.build_year = 1900
        surface.distance_gemengd_riool = 3
        surface.distance_hemelwaterriool = 3
        surface.distance_infiltratievoorziening = 1
        it.decision_tree(surface, parameters)                

        # Gemengd plus hwa of infiltratie, oud pand 
        # Altijd 100 of dichtsbijzijnde
        reset_surface()
        parameters.afkoppelen_hellende_daken = True
        surface.surface_type = 'pand'
        surface.build_year = 1900
        surface.distance_gemengd_riool = 3
        surface.distance_hemelwaterriool = 3
        surface.distance_infiltratievoorziening = 1
        it.decision_tree(surface, parameters)

        # Gemengd plus hwa of infiltratie, oud pand, maar niet afkoppelen hellende daken 
        # Altijd gemengd
        reset_surface()
        parameters.afkoppelen_hellende_daken = False
        surface.surface_type = 'pand'
        surface.build_year = 1900
        surface.distance_gemengd_riool = 3
        surface.distance_hemelwaterriool = 3
        surface.distance_infiltratievoorziening = 1
        it.decision_tree(surface, parameters)

        # Geen afgekoppeld systeem dus: infiltratie + rwa of alleen gemengd, alleen rwa of alleen infiltratie 
        reset_surface()
        surface.surface_type = 'pand'
        surface.build_year = 1900
        surface.distance_gemengd_riool = 1
        it.decision_tree(surface, parameters)

        reset_surface()
        surface.surface_type = 'pand'
        surface.build_year = 1900
        surface.distance_hemelwaterriool = 1
        it.decision_tree(surface, parameters)

        reset_surface()
        surface.surface_type = 'pand'
        surface.build_year = 1900
        surface.distance_infiltratievoorziening = 1
        it.decision_tree(surface, parameters)

        reset_surface()
        surface.surface_type = 'pand'
        surface.build_year = 1900
        surface.distance_oppervlaktewater = 3
        it.decision_tree(surface, parameters)
        
        # Geen bouwwerk, wel verhard
        # Gemengd riool
        reset_surface()
        surface.surface_type = None
        surface.type_verharding = 'verhard'
        surface.distance_gemengd_riool = 1
        it.decision_tree(surface, parameters)

        # alleen rwa of infiltratie
        reset_surface()
        surface.surface_type = None
        surface.type_verharding = 'verhard'
        surface.distance_hemelwaterriool = 1
        it.decision_tree(surface, parameters)        

        reset_surface()
        surface.surface_type = None
        surface.type_verharding = 'verhard'
        surface.distance_infiltratievoorziening = 1
        it.decision_tree(surface, parameters)        
        
        # infiltratie + rwa 
        reset_surface()
        surface.surface_type = None
        surface.type_verharding = 'verhard'
        surface.distance_infiltratievoorziening = 1
        surface.distance_hemelwaterriool = 0.5
        it.decision_tree(surface, parameters)        
        
        # infiltratie + gemengd + hwa
        reset_surface()
        surface.surface_type = None
        surface.type_verharding = 'verhard'
        surface.distance_infiltratievoorziening = 2
        surface.distance_hemelwaterriool = 2
        surface.distance_gemengd_riool = 1
        it.decision_tree(surface, parameters)
        
        # infiltratie + gemengd + hwa
        reset_surface()
        surface.surface_type = None
        surface.type_verharding = 'verhard'
        surface.distance_hemelwaterriool = 40
        surface.distance_gemengd_riool = 1
        it.decision_tree(surface, parameters)
        
        reset_surface()
        surface.surface_type = None
        surface.type_verharding = 'verhard'
        surface.distance_oppervlaktewater = 100
        it.decision_tree(surface, parameters)

        
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
