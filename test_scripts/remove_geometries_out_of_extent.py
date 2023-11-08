# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 09:41:42 2023

@author: ruben.vanderzaag
"""

import geopandas as gpd
from shapely.geometry import Polygon
import os
from osgeo import ogr

os.chdir(r'G:\Projecten Y (2023)\Y0127 - BGT Inlooptabel Nieuwe Versie 2024\Gegevens\Bewerking\testdata')

#STEP 1: import extent as wkt
# Load the shapefile
shapefile_path = 'extent_zeewolde.shp'
gdf = gpd.read_file(shapefile_path)

# Assuming you want to convert the first geometry in the shapefile
geometry_to_convert = gdf['geometry'].iloc[0]
polygon = Polygon(geometry_to_convert)

# Convert geometry to WKT
wkt_representation = polygon.wkt

print("WKT representation of the geometry:")
print(wkt_representation)
wkt_envelope = wkt_representation
envelope_geometry = ogr.CreateGeometryFromWkt(wkt_envelope)

#PART2: import gpkg's as ogr.layer 


#GWSW leidingen
# Path to the Geopackage file
gpkg_path = 'gwsw_zeewolde.gpkg'

# Open the Geopackage
gpkg_ds = ogr.Open(gpkg_path, 0)  # 0 means read-only mode

# Check if the Geopackage was successfully opened
if gpkg_ds is None:
    print("Failed to open the Geopackage.")
else:
    print("Successfully opened the Geopackage.")
    layername = {}
    # Iterate over all layers in the Geopackage and print their names
    for i in range(gpkg_ds.GetLayerCount()):
        locals()["gwsw_layer_"+str(i)] = gpkg_ds.GetLayerByIndex(i)
        layer = locals()["gwsw_layer_"+str(i)]
        #layer = gpkg_ds.GetLayerByIndex(i)
        print(f"Layer {i}: {layer.GetName()}")

#BGT vlakken
# Path to the Geopackage file
gpkg_path = 'bgt_zeewolde_handmatig.gpkg'

# Open the Geopackage
gpkg_ds_BGT = ogr.Open(gpkg_path, 0)  # 0 means read-only mode

# Check if the Geopackage was successfully opened
if gpkg_ds is None:
    print("Failed to open the Geopackage.")
else:
    print("Successfully opened the Geopackage.")
    layername = {}
    # Iterate over all layers in the Geopackage and print their names
    for i in range(gpkg_ds_BGT.GetLayerCount()):
        locals()["BGT_layer_"+str(i)] = gpkg_ds_BGT.GetLayerByIndex(i)
        layer = locals()["BGT_layer_"+str(i)]
        #layer = gpkg_ds.GetLayerByIndex(i)
        print(f"Layer {i}: {layer.GetName()}")


#PART 3: remove_input_features_outside_clip_extent

#hiervoor is rtree nodig --> spatial indexing. Kan het voor het testen ook zonder??
def create_index(layer):
    layer.ResetReading()
    index = rtree.index.Index(interleaved=False)
    for feature in layer:
        if feature:
            geometry = feature.GetGeometryRef()
            xmin, xmax, ymin, ymax = geometry.GetEnvelope()
            index.insert(feature.GetFID(), (xmin, xmax, ymin, ymax))
        else:
            pass

    return index

pipes = gwsw_layer_1
bgt_surfaces = BGT_layer_1

intersecting_pipes = []
non_intersecting_pipes =[]
intersecting_surfaces = []
#pipe_id = 0
#surface_id = 0
for pipe in pipes:
    #pipe = pipes.GetFeature(pipe_id)
    pipe_fid = pipe.GetFID()
    pipe_geom = pipe.geometry()
    if pipe_geom.Intersects(envelope_geometry):
        intersecting_pipes.append(pipe_fid)
        #pipe_id +=1
    else: 
        non_intersecting_pipes.append(pipe_fid)
        #pipe_id +=1

for surface in bgt_surfaces:
    surface_fid = surface.GetFID()
    surface_geom = surface.geometry()
    if surface_geom.Intersects(envelope_geometry):
        intersecting_surfaces.append(surface_fid)
        #surface_id +=1

for pipe in pipes:
    pipe_fid = pipe.GetFID()
    if pipe_fid not in intersecting_pipes:
        pipes.DeleteFeature(pipe_fid)

for surface in bgt_surfaces:
    surface_fid = surface.GetFID()
    if surface_fid not in intersecting_surfaces:
        bgt_surfaces.DeleteFeature(surface_fid)
        
#PART 4: write OGR.layers to shapefile to inspect in QGIS - werkt nog niet!
# Create a new shapefile
output_shapefile_path = 'output_shapefile_bgt.shp'
output_driver = ogr.GetDriverByName('ESRI Shapefile')
output_ds = output_driver.CreateDataSource(output_shapefile_path)
input_layer = gpkg_ds_BGT.GetLayerByIndex(1)
layer_metadata = input_layer.GetLayerDefn()
# Create a new layer in the shapefile
output_layer = output_ds.CreateLayer('bgt', input_layer.GetSpatialRef(), input_layer.GetGeomType())

# Copy the fields from the input layer to the output layer
for i in range(layer_metadata.GetFieldCount()):
    field_def = layer_metadata.GetFieldDefn(i)
    output_layer.CreateField(field_def)

# Copy the features from the input layer to the output layer
for feature in input_layer:
    output_layer.CreateFeature(feature)