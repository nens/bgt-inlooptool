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
DATA_PATH = "C:/Users/chris.kerklaan/Documents/Github/bgt-inlooptool/test-data"
__file__ = "C:/Users/chris.kerklaan/Documents/Github/bgt-inlooptool/core/inlooptool.py"
DATA_PATH = os.path.dirname(__file__).replace('core','test-data')

# Find package
sys.path.append(os.path.dirname(__file__).replace('/core', ''))

# Local/test imports
from core.inlooptool import Database
from core.inlooptool import InputParameters
from core.constants import ALL_USED_SURFACE_TYPES

class UnitDatabase(unittest.TestCase):
    """ used for both unittests and integrated testing"""
    
    def test_loading(self):
        """ Test database loading using different assert"""
        self.db = Database()
        
        """ Tests if the surfaces have a ogr layer loaded into the memory db"""
        self.db.load_surfaces(os.path.join(DATA_PATH, 'extract.zip'))
        
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
                
        """ Tests if epsg is properly registered"""        
        self.db.register_epsg()
        
        sql = "SELECT * FROM gpkg_spatial_ref_sys WHERE srs_id = 28992"
        layer = self.db.mem_database.ExecuteSQL(sql)        
        self.assertTrue(layer[0]['srs_id'] == 28992,"registering failure, srs not 28992")
        
        """ Tests if contents are properly registered"""
        self.db.register_surfaces()
        
        for surface_type in ALL_USED_SURFACE_TYPES:    
            sql = "SELECT * FROM gpkg_contents WHERE table_name = '{}';".format(surface_type )
            layer = self.db.mem_database.ExecuteSQL(sql)
            self.assertTrue(layer[0]['table_name'] == surface_type,
                           "gpkg contents not registered")
            
    def test_classify(self):
        db = Database()        
        db.import_surfaces(os.path.join(DATA_PATH, 'extract.zip'))
        
        self.assertTrue(db.bgt_surfaces is not None,
                            "db.bgt_surfaces is None")
        
            
        parameters = InputParameters()
        db.classify_surfaces(parameters)
        
        """ Tests if all features are classified"""
        for feature in self.db.bgt_surfaces:
            self.assertTrue(feature['type_verharding'] is not None,
                            "type verharding is None")
            self.assertTrue(feature['graad_verharding'] is not None,
                            "graad verharding is None")
            
    
    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
