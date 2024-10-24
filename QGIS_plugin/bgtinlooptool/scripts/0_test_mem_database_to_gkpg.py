# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 09:51:04 2024

@author: ruben.vanderzaag
"""
from osgeo import ogr, gdal
import contextlib

def import_gpkg_to_db(gpkg_file):
    
    # Register all drivers
    gdal.AllRegister()
    MEM_DRIVER = ogr.GetDriverByName("Memory")
    
    # Open the GeoPackage file
    datasource = ogr.Open(gpkg_file, 0)  # 0 means read-only, 1 means read-write
    
    if datasource is None:
        print("Failed to open the GeoPackage file.")
    else:
        print("GeoPackage file opened successfully.")
    
    # Get the number of layers
    layer_count = datasource.GetLayerCount()
    print(f"Number of layers: {layer_count}")
    
    # Create the output datasource
    output_datasource = MEM_DRIVER.CreateDataSource("")
    
    # Iterate over each layer
    for i in range(layer_count):
        layer = datasource.GetLayerByIndex(i)
        layer_name = layer.GetName()
        print(f"Layer {i}: {layer_name}")
    
        # Create a new layer in the output datasource
        output_layer = output_datasource.CreateLayer(layer_name, geom_type=layer.GetGeomType())
    
        # Get the layer definition
        layer_defn = layer.GetLayerDefn()
    
        # Add fields to the output layer
        for j in range(layer_defn.GetFieldCount()):
            field_defn = layer_defn.GetFieldDefn(j)
            output_layer.CreateField(field_defn)
    
        # Copy features from the input layer to the output layer
        for feature in layer:
            output_layer.CreateFeature(feature)
    
    # Close the datasource
    datasource = None
    return output_datasource

def _write_to_disk(file_path, db_layer_name, dst_layer_name): 
    """Copy mem_database to file_path"""
    # Get the source layer from the memory database
    db_layer = mem_database.GetLayerByName(db_layer_name)
    if db_layer is None:
        raise ValueError(f"Layer '{db_layer_name}' not found in memory database.")
    
    # Open the destination GeoPackage in write mode
    dst_gpkg = GPKG_DRIVER.Open(file_path, 1)  # 1 means writable
    if dst_gpkg is None:
        raise ValueError(f"Could not open GeoPackage '{file_path}' for writing.")
    
    # Get the destination layer from the GeoPackage
    dst_layer = dst_gpkg.GetLayerByName(dst_layer_name)
    if dst_layer is None:
        raise ValueError(f"Layer '{dst_layer_name}' not found in destination GeoPackage.")
    
    # Get the layer definitions for both the source and destination layers
    layer_defn = db_layer.GetLayerDefn()
    dst_layer_defn = dst_layer.GetLayerDefn()
    
    # Optional: Check if field counts are consistent
    if layer_defn.GetFieldCount() != dst_layer_defn.GetFieldCount():
        print(f"Warning: Source and destination layers have different field counts: {layer_defn.GetFieldCount()} vs {dst_layer_defn.GetFieldCount()}")
    
    # Create a mapping from destination field names to source field indices
    field_mapping = {}
    for i in range(dst_layer_defn.GetFieldCount()):
        dst_field_name = dst_layer_defn.GetFieldDefn(i).GetName()
        for j in range(layer_defn.GetFieldCount()):
            src_field_name = layer_defn.GetFieldDefn(j).GetName()
            if dst_field_name == src_field_name:
                field_mapping[dst_field_name] = j
                break
    
    # Copy features while maintaining the field order
    for feature in db_layer:
        dst_feature = ogr.Feature(dst_layer_defn)
        for dst_field_name, src_field_index in field_mapping.items():
            value = feature.GetField(src_field_index)
            dst_feature.SetField(dst_field_name, value)
    
        # Copy geometry from source feature to destination feature
        geom = feature.GetGeometryRef()
        if geom:
            dst_feature.SetGeometry(geom.Clone())
        else:
            print("No geometry found for feature.")
    
        # Create the feature in the destination layer
        dst_layer.CreateFeature(dst_feature)
        dst_feature = None  # Free resources
    # Clean up
    dst_gpkg = None
    dst_layer = None
    db_layer = None
    print("Done with saving")

@contextlib.contextmanager
def open_gpkg(file_path):
    dst_gpkg = GPKG_DRIVER.Open(file_path, 1)
    if dst_gpkg is None:
        raise ValueError(f"Could not open GeoPackage '{file_path}' for writing.")
    try:
        yield dst_gpkg
    finally:
        dst_gpkg = None

# Drivers
GPKG_DRIVER = ogr.GetDriverByName("GPKG")
MEM_DRIVER = ogr.GetDriverByName("Memory")

#mem_database gpkg path:
file_path = r"C:\Users\ruben.vanderzaag\Documents\Github\bgt-inlooptool\QGIS_plugin\bgtinlooptool\style\output_bgtinlooptool_mem_db.gpkg"

#create mem_database (ogr datasource object)
mem_database = import_gpkg_to_db(file_path)

#test function
output_gpkg = r"output_path" #=copy of empty template output gpkg
db_layer_name = "bgt_inlooptabel"
dst_layer_name = "4. BGT inlooptabel"
_write_to_disk(output_gpkg,db_layer_name,dst_layer_name)


#Test new function (start after with): 
db_layer = mem_database.GetLayerByName(db_layer_name)
if db_layer is None:
    raise ValueError(f"Layer '{db_layer_name}' not found in memory database.")

file_path =r"C:\Users\ruben.vanderzaag\Documents\Github\bgt-inlooptool\QGIS_plugin\bgtinlooptool\style\output_bgtinlooptabel_test2.gpkg"
with open_gpkg(file_path) as dst_gpkg:
    db_layer_name = "bgt_inlooptabel"
    dst_layer_name = "4. BGT inlooptabel"


