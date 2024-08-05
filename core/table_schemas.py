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
        "surface_type": ogr.OFTString,
        "bgt_fysiek_voorkomen": ogr.OFTString,
        "build_year": ogr.OFTInteger,
        RESULT_TABLE_FIELD_WIJZIGING: ogr.OFTInteger,
    },
    primary_key="id",
    geometry_column="geom",
    geometry_type=ogr.wkbCurvePolygon,
)


SETTINGS_TABLE_SCHEMA = TableSchema(
    fields={
        #"fid": ogr.OFTInteger,
        SETTINGS_TABLE_FIELD_ID: ogr.OFTInteger,
        SETTINGS_TABLE_FIELD_TIJD_START: ogr.OFTDateTime,
        SETTINGS_TABLE_FIELD_TIJD_EIND: ogr.OFTDateTime,  
        SETTINGS_TABLE_FIELD_DOWNLOAD_BGT:ogr.OFTInteger,
        SETTINGS_TABLE_FIELD_DOWNLOAD_GWSW:ogr.OFTInteger,
        SETTINGS_TABLE_FIELD_DOWNLOAD_BAG:ogr.OFTInteger,
        SETTINGS_TABLE_FIELD_PAD_BGT: ogr.OFTString,
        SETTINGS_TABLE_FIELD_PAD_GWSW: ogr.OFTString,
	SETTINGS_TABLE_FIELD_PAD_BAG: ogr.OFTString,
        SETTINGS_TABLE_FIELD_PAD_KOLKEN: ogr.OFTString,
        SETTINGS_TABLE_FIELD_AFSTAND_AFWATERINGSVOORZIENING: ogr.OFTReal,
        SETTINGS_TABLE_FIELD_AFSTAND_VERHARD_OPP_WATER: ogr.OFTReal,
        SETTINGS_TABLE_FIELD_AFSTAND_PAND_OPP_WATER: ogr.OFTReal,
        SETTINGS_TABLE_FIELD_AFSTAND_VERHARD_KOLK: ogr.OFTReal,
        SETTINGS_TABLE_FIELD_AFSTAND_AFKOPPELD: ogr.OFTReal,
        SETTINGS_TABLE_FIELD_AFSTAND_DRIEVOUDIG: ogr.OFTReal,
        SETTINGS_TABLE_FIELD_VERHARDINGSGRAAD_ERF: ogr.OFTReal,
        SETTINGS_TABLE_FIELD_VERHARDINGSGRAAD_HALF_VERHARD: ogr.OFTReal,
        SETTINGS_TABLE_FIELD_AFKOPPELEN_HELLEND: ogr.OFTReal,
        SETTINGS_TABLE_FIELD_BOUWJAAR_GESCHEIDEN_BINNENHUIS: ogr.OFTInteger,
    },
    primary_key="run_id",
    geometry_column="", #settings table has no geometry
    geometry_type=ogr.wkbNone,
)

STATISTICS_TABLE_SCHEMA = TableSchema(
    fields={
        #"fid": ogr.OFTInteger,
        STATISTICS_TABLE_FIELD_ID: ogr.OFTInteger,
        STATISTICS_TABLE_FIELD_OPP_TOTAAL: ogr.OFTReal,
        STATISTICS_TABLE_FIELD_OPP_GEMENGD: ogr.OFTReal,  
        STATISTICS_TABLE_FIELD_OPP_HWA:ogr.OFTReal,
        STATISTICS_TABLE_FIELD_OPP_VGS:ogr.OFTReal,
        STATISTICS_TABLE_FIELD_OPP_DWA:ogr.OFTReal,
        STATISTICS_TABLE_FIELD_OPP_INFIL: ogr.OFTReal,
        STATISTICS_TABLE_FIELD_OPP_OPEN_WATER: ogr.OFTReal,
	STATISTICS_TABLE_FIELD_OPP_MAAIVELD: ogr.OFTReal,
        STATISTICS_TABLE_FIELD_PERC_GEMENGD: ogr.OFTReal,  
        STATISTICS_TABLE_FIELD_PERC_HWA:ogr.OFTReal,
        STATISTICS_TABLE_FIELD_PERC_VGS:ogr.OFTReal,
        STATISTICS_TABLE_FIELD_PERC_DWA:ogr.OFTReal,
        STATISTICS_TABLE_FIELD_PERC_INFIL: ogr.OFTReal,
        STATISTICS_TABLE_FIELD_PERC_OPEN_WATER: ogr.OFTReal,
	STATISTICS_TABLE_FIELD_PERC_MAAIVELD: ogr.OFTReal,
    },
    primary_key="id",
    geometry_column="geom",
    geometry_type=ogr.wkbCurvePolygon,
)