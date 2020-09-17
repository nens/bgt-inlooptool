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
DATA_PATH = os.path.join(os.path.dirname(__file__), "../test-data")
SURFACES_INPUT_FILENAME = os.path.join(DATA_PATH, 'extract.zip')
PIPES_INPUT_FILENAME = os.path.join(DATA_PATH, 'getGeoPackage_1134.gpkg')

# Find package
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.append(os.path.dirname(__file__))

# Local/test imports
from core.inlooptool import *
from core.constants import *


class UnitDatabase(unittest.TestCase):
    """ used for both unittests and integrated testing"""

    # def empty_result_table(self):
    #     """Can the Database succesfully generate an empty result table?"""
    #     self.db = Database()
    #     out_gpkg_fn = os.path.join(DATA_PATH, 'empty_result.gpkg')
    #     if os.path.exists(out_gpkg_fn):
    #         os.remove(out_gpkg_fn)
    #     hard_gpkg_ds = GPKG_DRIVER.CreateDataSource(out_gpkg_fn)
    #     src_lyr = self.db.result_table
    #     hard_gpkg_ds.CopyLayer(src_lyr, RESULT_TABLE_NAME)
    #     hard_gpkg_ds = None
    #     result = ogr.Open(out_gpkg_fn)
    #     self.assertTrue(isinstance(result, ogr.DataSource), 'empty_result.gpkg is not a valid ogr.Datasource')
    #
    # def test_import_surfaces(self):
    #     """ Test _database loading using different assert"""
    #     self.db = Database()
    #
    #     """ Tests if the surfaces have a ogr layer loaded into the memory db"""
    #     self.db.import_surfaces_raw(SURFACES_INPUT_FILENAME)
    #
    #     checks = []
    #     for surface_type in ALL_USED_SURFACE_TYPES:
    #         layer = self.db.mem_database.GetLayerByName(surface_type)
    #         if layer is not None:
    #             checks.append(True)
    #     self.assertTrue(
    #         len(checks) == len(ALL_USED_SURFACE_TYPES),
    #         "not all layers are loaded into the memory db"
    #     )
    #
    #     """ Tests if all loaded surfaces are a polygon"""
    #     self.db.clean_surfaces()
    #
    #     for surface_type in ALL_USED_SURFACE_TYPES:
    #         layer = self.db.mem_database.GetLayerByName(surface_type)
    #         for feature in layer:
    #             geom = feature.geometry()
    #             geom_type = geom.GetGeometryType()
    #             self.assertTrue(
    #                 geom_type == ogr.wkbPolygon,
    #                 "geometry in layer {} is not a polygon".format(surface_type)
    #             )
    #
    #     """ Tests if epsg is properly registered"""
    #     self.db.register_epsg()
    #
    #     sql = "SELECT * FROM gpkg_spatial_ref_sys WHERE srs_id = 28992"
    #     layer = self.db.mem_database.ExecuteSQL(sql)
    #     self.assertTrue(layer[0]['srs_id'] == 28992, "registering failure, srs not 28992")
    #
    #     """ Tests if contents are properly registered"""
    #     self.db.register_surfaces()
    #
    #     for surface_type in ALL_USED_SURFACE_TYPES:
    #         sql = "SELECT * FROM gpkg_contents WHERE table_name = '{}';".format(surface_type)
    #         layer = self.db.mem_database.ExecuteSQL(sql)
    #         self.assertTrue(layer[0]['table_name'] == surface_type,
    #                         "gpkg contents not registered")
    #
    # def test_classify(self):
    #     params = InputParameters()
    #     it = BGTInloopTool(params)
    #     db = it._database
    #     it.import_surfaces(SURFACES_INPUT_FILENAME)
    #
    #     self.assertTrue(db.bgt_surfaces is not None,
    #                     "db.bgt_surfaces is None")
    #
    #     parameters = InputParameters()
    #     db.classify_surfaces(parameters)
    #
    #     """ Tests if all features are classified"""
    #     for feature in db.bgt_surfaces:
    #         self.assertTrue(feature['type_verharding'] is not None,
    #                         "type verharding is None")
    #
    # def test_import_pipes(self):
    #     params = InputParameters()
    #     it = BGTInloopTool(params)
    #     db = it._database
    #     it.import_pipes(file_path=PIPES_INPUT_FILENAME)
    #     self.assertTrue(db.pipes.GetFeatureCount() == 8986)

    def test_calculate_runoff_targets(self):
        params = InputParameters()
        it = BGTInloopTool(params)
        it.import_surfaces(file_path=SURFACES_INPUT_FILENAME)
        it.import_pipes(file_path=PIPES_INPUT_FILENAME)
        it._database._write_to_disk(file_path=os.path.join(DATA_PATH, 'mem_dump.gpkg'))
        # it.calculate_distances(params)
        # it.calculate_runoff_targets()
        # out_gpkg_fn = os.path.join(DATA_PATH, 'calculated_result.gpkg')
        # if os.path.exists(out_gpkg_fn):
        #     os.remove(out_gpkg_fn)
        # hard_gpkg_ds = GPKG_DRIVER.CreateDataSource(out_gpkg_fn)
        # src_lyr = it._database.result_table
        # hard_gpkg_ds.CopyLayer(src_lyr, RESULT_TABLE_NAME)
        # hard_gpkg_ds = None
        # result = ogr.Open(out_gpkg_fn)
        # self.assertTrue(isinstance(result, ogr.DataSource), 'calculated_result.gpkg is not a valid ogr.Datasource')


if __name__ == '__main__':
    unittest.main()
