from osgeo import ogr
from core.constants import *


class TableSchema:
    def __init__(self, fields, primary_key, geometry_column, geometry_type):
        self.fields = fields
        self.pk = primary_key
        self.geometry_column = geometry_column
        self.geometry_type = geometry_type


surfaces_table_fields = {
    "id": ogr.OFTInteger,
    "identificatie_lokaalid": ogr.OFTString,
    "surface_type": ogr.OFTString,
    "bgt_fysiek_voorkomen": ogr.OFTString,
    RESULT_TABLE_FIELD_TYPE_VERHARDING: ogr.OFTString,
    RESULT_TABLE_FIELD_GRAAD_VERHARDING: ogr.OFTReal,
    "build_year": ogr.OFTInteger,
    "identificatiebagpnd": ogr.OFTString,
}
for dist_type in DISTANCE_TYPES:
    surfaces_table_fields["distance_" + dist_type] = ogr.OFTReal
del dist_type

SURFACES_TABLE_SCHEMA = TableSchema(
    surfaces_table_fields,
    primary_key="id",
    geometry_column="geom",
    geometry_type=ogr.wkbPolygon,
)

RESULT_TABLE_SCHEMA = TableSchema(
    fields={
        RESULT_TABLE_FIELD_ID: ogr.OFTInteger,
        RESULT_TABLE_FIELD_LAATSTE_WIJZIGING: ogr.OFTDateTime,
        RESULT_TABLE_FIELD_BGT_IDENTIFICATIE: ogr.OFTString,
        RESULT_TABLE_FIELD_TYPE_VERHARDING: ogr.OFTString,
        RESULT_TABLE_FIELD_GRAAD_VERHARDING: ogr.OFTReal,
        RESULT_TABLE_FIELD_HELLINGSTYPE: ogr.OFTString,
        RESULT_TABLE_FIELD_HELLINGSPERCENTAGE: ogr.OFTReal,
        # RESULT_TABLE_FIELD_BERGING_DAK: ogr.OFTReal,
        RESULT_TABLE_FIELD_TYPE_PRIVATE_VOORZIENING: ogr.OFTString,
        RESULT_TABLE_FIELD_BERGING_PRIVATE_VOORZIENING: ogr.OFTReal,
        RESULT_TABLE_FIELD_CODE_VOORZIENING: ogr.OFTString,
        RESULT_TABLE_FIELD_PUTCODE: ogr.OFTString,
        RESULT_TABLE_FIELD_LEIDINGCODE: ogr.OFTString,
        TARGET_TYPE_GEMENGD_RIOOL: ogr.OFTReal,
        TARGET_TYPE_HEMELWATERRIOOL: ogr.OFTReal,
        TARGET_TYPE_VGS_HEMELWATERRIOOL: ogr.OFTReal,
        TARGET_TYPE_VUILWATERRIOOL: ogr.OFTReal,
        TARGET_TYPE_INFILTRATIEVOORZIENING: ogr.OFTReal,
        TARGET_TYPE_OPEN_WATER: ogr.OFTReal,
        TARGET_TYPE_MAAIVELD: ogr.OFTReal,
    },
    primary_key="id",
    geometry_column="geom",
    geometry_type=ogr.wkbCurvePolygon,
)
