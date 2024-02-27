# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 09:36:30 2023

@author: ruben.vanderzaag
"""
# System imports
import os
import sys

# Third-party imports
from osgeo import osr
from osgeo import gdal
from osgeo import ogr
from datetime import datetime

# Rtree should be installed by the plugin for QGIS
# For ArcGIS Pro the following is needed
import sys
from pathlib import Path
from .rtree_installer import unpack_rtree
if not str(Path(__file__).parent) in sys.path:  # bgt_inlooptool\\core
    rtree_path = unpack_rtree()
    sys.path.append(str(rtree_path))

import rtree

# Local imports
from core.table_schemas import *
from core.constants import *
from core.constants import (
    ALL_USED_SURFACE_TYPES,
    MULTIPLE_GEOMETRY_SURFACE_TYPES,
    SURFACES_TABLE_NAME,
    RESULT_TABLE_FIELD_GRAAD_VERHARDING,
    RESULT_TABLE_FIELD_TYPE_VERHARDING,
    SURFACE_TYPE_PAND,
    VERHARDINGSTYPE_PAND,
    SURFACE_TYPE_WATERDEEL,
    VERHARDINGSTYPE_WATER,
    PIPES_TABLE_NAME,
)
from core.defaults import *

# Globals
GFS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gfs")

# Exceptions
gdal.UseExceptions()
ogr.UseExceptions()

#Merge BGT Zip
def __init__(self, epsg=28992):
    """
    Constructor
    :param epsg: srid / EPSG code
    """
    self.epsg = epsg
    self.srs = osr.SpatialReference()
    self.srs.ImportFromEPSG(epsg)
    self.mem_database = MEM_DRIVER.CreateDataSource("")
    self.create_table(
        table_name=RESULT_TABLE_NAME, table_schema=RESULT_TABLE_SCHEMA
    )

@property
def result_table(self):
    """Get reference to result layer (BGT Inlooptabel)
    :rtype ogr.Layer
    """
    return self.mem_database.GetLayerByName(RESULT_TABLE_NAME)

@property
def bgt_surfaces(self):
    """Get reference to BGT Surface layer
    :rtype ogr.Layer
    """
    return self.mem_database.GetLayerByName(SURFACES_TABLE_NAME)

@property
def pipes(self):
    """Get reference to Pipes layer
    :rtype ogr.Layer
    """
    return self.mem_database.GetLayerByName(PIPES_TABLE_NAME)

@property
def kolken(self):
    """Get reference to Kolken layer
    :rtype ogr.Layer
    """
    return self.mem_database.GetLayerByName(KOLKEN_TABLE_NAME)

@property
def buildings(self):
    """Get reference to Pipes layer
    :rtype ogr.Layer
    """
    return self.mem_database.GetLayerByName(BUILDINGS_TABLE_NAME)

def create_table(table_name, table_schema):
    """Create or replace the result table
    :param table_schema:
    :param table_name:
    """
    lyr = mem_database.CreateLayer(
        table_name, srs, geom_type=table_schema.geometry_type
    )

    for fieldname, datatype in table_schema.fields.items():
        field_defn = ogr.FieldDefn(fieldname, datatype)
        lyr.CreateField(field_defn)

    lyr = None

def import_pipes(self, file_path):
    """
    Copy the required contents of the GWSW GeoPackage file to self.mem_database
    :param file_path: GWSW GeoPackage
    :return: None
    """
    gwsw_gpkg_abspath = os.path.abspath(file_path)
    if not os.path.isfile(gwsw_gpkg_abspath):
        raise FileNotFoundError(
            "GWSW GeoPackage niet gevonden: {}".format(gwsw_gpkg_abspath)
        )
    lines_ds = ogr.Open(file_path)
    # TODO more thorough checks of validity of input geopackage
    try:
        self.mem_database.CopyLayer(
            lines_ds.GetLayerByName(SOURCE_PIPES_TABLE_NAME), PIPES_TABLE_NAME
        )
    except Exception:
        # TODO more specific exception
        raise FileInputError(
            "Ongeldige input: {} is geen geldige GWSW GeoPackage".format(
                gwsw_gpkg_abspath
            )
        )

def import_surfaces_raw(file_path):
    """
    Copy the required contents of the BGT zip file 'as is' to self.mem_database
    :param file_path:
    :return: None
    """
    bgt_zip_file_abspath = os.path.abspath(file_path)
    if not os.path.isfile(bgt_zip_file_abspath):
        raise FileNotFoundError(
            "BGT zip niet gevonden: {}".format(bgt_zip_file_abspath)
        )

    try:
        nr_layers_with_features = 0
        for stype in ALL_USED_SURFACE_TYPES:
            surface_source_fn = os.path.join(
                "/vsizip/" + file_path, "bgt_{stype}.gml".format(stype=stype)
            )
            if stype in MULTIPLE_GEOMETRY_SURFACE_TYPES:
                surface_source_gfs_fn = os.path.join(GFS_DIR, f"bgt_{stype}.gfs")
                if not os.path.isfile(surface_source_gfs_fn):
                    raise ValueError(f"GFS file for {stype} not found")
                surface_source = gdal.OpenEx(
                    surface_source_fn,
                    open_options=[f"GFS_TEMPLATE={surface_source_gfs_fn}"],
                )
            else:
                surface_source = ogr.Open(surface_source_fn)
            if surface_source is None:
                continue  # TODO Warning
            else:
                src_layer = surface_source.GetLayerByName(
                    "{stype}".format(stype=stype)
                )
                if src_layer is None:
                    continue  # TODO Warning
                else:
                    nr_layers_with_features += 1
                    mem_database.CopyLayer(src_layer=src_layer, new_name=stype)
                    print(f"raw import of {stype} layer has {mem_database.GetLayerByName(stype).GetFeatureCount()} features")
        if nr_layers_with_features == 0:
            raise FileInputError(
                f"BGT zip file is leeg of bevat alleen lagen zonder features"
            )
    except FileInputError:
        raise
    except Exception:
        raise FileInputError(f"Probleem met laag {stype}.gml in BGT zip file")

def import_kolken(self, file_path):

    """
    Copy point features from a ogr layer

    """
    kolken_abspath = os.path.abspath(file_path)
    if not os.path.isfile(kolken_abspath):
        raise FileNotFoundError("Bestand niet gevonden: {}".format(kolken_abspath))
    # TODO more thorough checks of validity of input geopackage

    try:
        kolken_ds = ogr.Open(file_path)
        self.mem_database.CopyLayer(kolken_ds[0], KOLKEN_TABLE_NAME)
    except Exception:
        # TODO more specific exception
        raise FileInputError("Ongeldige input: {}".format(kolken_abspath))

def add_index_to_inputs(self, pipes=True, bgt_surfaces=True, kolken=True):
    """
    add index to input layers if rtree is installed

    """
    self.pipes_idx = create_index(self.pipes)
    self.bgt_surfaces_idx = create_index(self.bgt_surfaces)
    if kolken:
        self.kolken_idx = create_index(self.kolken)

def remove_input_features_outside_clip_extent(self, extent_wkt):

    extent_geometry = ogr.CreateGeometryFromWkt(extent_wkt)
    
    pipes = self.pipes
    bgt_surfaces = self.bgt_surfaces

    intersecting_pipes = []
    intersecting_surfaces = []

    for pipe in pipes:
        pipe_fid = pipe.GetFID()
        pipe_geom = pipe.geometry()
        if pipe_geom.Intersects(extent_geometry):
            intersecting_pipes.append(pipe_fid)
  
    for surface in bgt_surfaces:
        surface_fid = surface.GetFID()
        surface_geom = surface.geometry()
        if surface_geom.Intersects(extent_geometry):
            intersecting_surfaces.append(surface_fid)

    for pipe in self.pipes:
        pipe_fid = pipe.GetFID()
        if pipe_fid not in intersecting_pipes:
            self.pipes.DeleteFeature(pipe_fid)

    for surface in self.bgt_surfaces:
        surface_fid = surface.GetFID()
        if surface_fid not in intersecting_surfaces:
            self.bgt_surfaces.DeleteFeature(surface_fid)

    pipes = None
    bgt_surfaces = None

def clean_surfaces(self):
    """
    Update the surfaces layer to include polygons only.
    Linestring features are removed.
    Multipolygons, multisurfaces, curved polygons are forced to polygon.

    """
    for surface_type in ALL_USED_SURFACE_TYPES:
        layer = mem_database.GetLayerByName(surface_type)
        if layer is None:  # this happens if this particular layer in the bgt input has no features
            continue
        layer.ResetReading()
        delete_fids = []
        for feature in layer:
            geom = feature.GetGeometryRef()
            geom_type = geom.GetGeometryType()
            if geom_type == ogr.wkbPolygon:
                pass
            elif geom_type in [ogr.wkbCurvePolygon, ogr.wkbMultiSurface]:
                # print('Fixing Curve Polygon feature {}'.format(f.GetFID()))
                geom_linear = geom.GetLinearGeometry()
                feature.SetGeometry(geom_linear)
                layer.SetFeature(feature)
            elif geom_type in (
                ogr.wkbLineString,
                ogr.wkbCompoundCurve,
                ogr.wkbCircularString,
            ):
                # print('Deleting feature {} because it is a Linestring'.format(f.GetFID()))
                delete_fids.append(feature.GetFID())
            else:
                print(
                    "Warning: Fixing feature {fid} in {stype} failed! No procedure defined to clean up geometry "
                    "type {geom_type}. Continuing anyway.".format(
                        fid=feature.GetFID(), stype=surface_type, geom_type=str(geom_type)
                    )
                )
                continue
        for fid in delete_fids:
            layer.DeleteFeature(fid)
        print(
            f"cleaned import of {surface_type} layer has {layer.GetFeatureCount()} features"
        )

        layer = None

def classify_pipes(self, delete=True):
    """Assign pipe type based on GWSW pipe type. Optionally, delete pipes of type INTERNAL_PIPE_TYPE_IGNORE"""
    layer = self.mem_database.GetLayerByName(PIPES_TABLE_NAME)
    if layer is None:
        raise DatabaseOperationError

    layer.CreateField(ogr.FieldDefn(INTERNAL_PIPE_TYPE_FIELD, ogr.OFTString))

    delete_fids = []
    for pipe_feat in layer:
        if pipe_feat:
            gwsw_pipe_type_uri = pipe_feat[GWSW_PIPE_TYPE_FIELD]
            gwsw_pipe_type_clean = gwsw_pipe_type_uri.split("/")[-1]
            try:
                internal_pipe_type = PIPE_MAP[gwsw_pipe_type_clean]
            except KeyError:
                internal_pipe_type = INTERNAL_PIPE_TYPE_IGNORE
            if internal_pipe_type == INTERNAL_PIPE_TYPE_IGNORE:
                delete_fids.append(pipe_feat.GetFID())
            elif internal_pipe_type == INTERNAL_PIPE_TYPE_HEMELWATERRIOOL:
                gwsw_stelsel_type_uri = pipe_feat[GWSW_STELSEL_TYPE_FIELD]
                gwsw_stelsel_type_clean = gwsw_pipe_type_uri.split("/")[-1]
                if (
                    gwsw_stelsel_type_clean
                    == GWSW_STELSEL_TYPE_VERBETERDHEMELWATERSTELSEL
                ):
                    internal_pipe_type = INTERNAL_PIPE_TYPE_VGS_HEMELWATERRIOOL
            pipe_feat[INTERNAL_PIPE_TYPE_FIELD] = internal_pipe_type
            layer.SetFeature(pipe_feat)

    if delete:
        for fid in delete_fids:
            layer.DeleteFeature(fid)

    layer = None

def classify_surfaces(self, parameters):
    """Determine NWRW surface type of all imported surfaces"""
    layer = mem_database.GetLayerByName(SURFACES_TABLE_NAME)
    if layer is None:
        raise DatabaseOperationError

    for feature in layer:
        if feature:
            verhardingsgraad = None
            verhardingstype = None
            if feature.surface_type == SURFACE_TYPE_PAND:
                verhardingstype = VERHARDINGSTYPE_PAND
                verhardingsgraad = 100
            elif feature.surface_type == SURFACE_TYPE_WATERDEEL:
                verhardingstype = VERHARDINGSTYPE_WATER
                verhardingsgraad = 0
            elif feature.surface_type == SURFACE_TYPE_ONDERSTEUNENDWATERDEEL:
                verhardingstype = VERHARDINGSTYPE_ONVERHARD
                verhardingsgraad = 0
            elif feature.surface_type in SURFACE_TYPES_MET_FYSIEK_VOORKOMEN:
                if feature.bgt_fysiek_voorkomen in (
                    "loofbos",
                    "heide",
                    "gemengd bos",
                    "groenvoorziening",
                    "transitie",
                    "rietland",
                    "grasland overig",
                    "houtwal",
                    "zand",
                    "moeras",
                    "fruitteelt",
                    "naaldbos",
                    "struiken",
                    "bouwland",
                    "duin",
                    "boomteelt",
                    "grasland agrarisch",
                    "onverhard",
                    "kwelder",
                ):
                    verhardingstype = VERHARDINGSTYPE_ONVERHARD
                    verhardingsgraad = 0
                elif feature.bgt_fysiek_voorkomen == "open verharding":
                    verhardingstype = VERHARDINGSTYPE_OPEN_VERHARD
                    verhardingsgraad = 100
                elif feature.bgt_fysiek_voorkomen == "half verhard":
                    verhardingstype = VERHARDINGSTYPE_OPEN_VERHARD
                    verhardingsgraad = 50
                elif feature.bgt_fysiek_voorkomen == "erf":
                    if 50 > 0:
                        verhardingstype = VERHARDINGSTYPE_OPEN_VERHARD
                    else:
                        verhardingstype = VERHARDINGSTYPE_ONVERHARD
                    verhardingsgraad = 50
                elif feature.bgt_fysiek_voorkomen == "gesloten verharding":
                    verhardingstype = VERHARDINGSTYPE_GESLOTEN_VERHARD
                    verhardingsgraad = 100
            feature[RESULT_TABLE_FIELD_TYPE_VERHARDING] = verhardingstype
            if verhardingsgraad is not None:
                feature[RESULT_TABLE_FIELD_GRAAD_VERHARDING] = verhardingsgraad
            layer.SetFeature(feature)
    layer = None

def merge_surfaces(self):
    """Merge and standardize all imported surfaces to one layer"""
    create_table(
        table_name=SURFACES_TABLE_NAME, table_schema=SURFACES_TABLE_SCHEMA
    )
    dest_layer = mem_database.GetLayerByName(SURFACES_TABLE_NAME)
    id_counter = 1
    previous_fcount = 0
    for stype in ALL_USED_SURFACE_TYPES:
        input_layer = mem_database.GetLayerByName(stype)
        if (
            input_layer is None
        ):  # this happens if this particular layer in the bgt input has no features
            continue
        for feature in input_layer:
            if hasattr(feature, "eindRegistratie"):
                if feature["eindRegistratie"] is not None:
                    continue
            if hasattr(feature, "plus-status"):
                if feature["plus-status"] in ["plan", "historie"]:
                    continue
            new_feature = ogr.Feature(dest_layer.GetLayerDefn())
            new_feature.SetField("id", id_counter)
            id_counter += 1
            new_feature.SetField(
                "identificatie_lokaalid", feature["identificatie.lokaalID"]
            )
            new_feature.SetField("surface_type", stype)

            if stype in SURFACE_TYPES_MET_FYSIEK_VOORKOMEN:
                new_feature["bgt_fysiek_voorkomen"] = feature["bgt-fysiekVoorkomen"]

            if stype == SURFACE_TYPE_PAND:
                new_feature["identificatiebagpnd"] = feature["identificatieBAGPND"]

            target_geometry = ogr.ForceToPolygon(feature.geometry())
            target_geometry.AssignSpatialReference(srs)
            new_feature.SetGeometry(target_geometry)
            dest_layer.CreateFeature(new_feature)
            target_geometry = None
            new_feature = None
        print(
            f"added {dest_layer.GetFeatureCount()-previous_fcount} features from {stype} layer"
        )
        previous_fcount = dest_layer.GetFeatureCount()
    dest_layer = None

def add_build_year_to_surface(self, file_path, field_name="bouwjaar"):

    print("Started add_build_year_to_surface...")

    ds = ogr.Open(file_path)
    buildings = ds[0]

    surfaces = self.bgt_surfaces
    surfaces.ResetReading()
    surfaces.CreateField(ogr.FieldDefn("build_year", ogr.OFTReal))

    # create dict from buildings
    building_dict = {}
    for building in buildings:
        building_dict[building["identificatie"][1:]] = building[field_name]
        building = None

    for surface in surfaces:
        if surface["surface_type"] == SURFACE_TYPE_PAND:
            if surface["identificatiebagpnd"] in building_dict.keys():
                surface["build_year"] = building_dict[
                    surface["identificatiebagpnd"]
                ]
                surfaces.SetFeature(surface)
        surface = None

    buildings = None
    surfaces = None
    print("... done")
    return

def _write_to_disk(self, file_path):
    """Copy self.mem_database to file_path"""
    self.out_db = GPKG_DRIVER.CopyDataSource(self.mem_database, file_path)
    self.out_db = None


class Layer(object):
    def __init__(self, layer):
        self.layer = layer
        self.layer_defn = layer.GetLayerDefn()

    def add_feature(self, geometry, attributes):
        """Append geometry and attributes as new feature."""
        feature = ogr.Feature(self.layer_defn)
        feature.SetGeometry(geometry)
        for key, value in attributes.items():
            feature[str(key)] = value
        self.layer.CreateFeature(feature)
        feature = None

    def add_field(self, name, _type):
        self.layer.CreateField(ogr.FieldDefn(name, _type))


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

def ogr_to_dataframe(layer):
    # Get the layer's feature definitions
    layer_defn = layer.GetLayerDefn()

    # Get field names
    field_names = [layer_defn.GetFieldDefn(i).GetName() for i in range(layer_defn.GetFieldCount())]

    # Initialize an empty list to store feature attributes
    data = []

    # Iterate over features and extract attributes
    for feature in layer:
        attributes = {field_name: feature.GetField(field_name) for field_name in field_names}
        data.append(attributes)

    # Convert the data to a DataFrame
    df = pd.DataFrame(data, columns=field_names)

    return df
import pandas as pd
dest_layer_merge_df = ogr_to_dataframe(dest_layer)
layer_clean_df = ogr_to_dataframe(layer) 
layer_classify_df =ogr_to_dataframe(layer) 

import_surfaces_raw(file_path) #check
clean_surfaces() #check
merge_surfaces() #check
classify_surfaces(parameters)