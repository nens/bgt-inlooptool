import os

import osr
from osgeo import ogr
from osgeo import gdal
from datetime import datetime

import numpy as np

import result_table_schema as schema
from constants import *

SQL_DIR = os.path.join(__file__, 'sql')

gdal.UseExceptions()
GPKG_DRIVER = ogr.GetDriverByName("GPKG")


class InputParameters:

    def __init__(self):
        self.max_afstand_vlak_afwateringsvoorziening = 40
        self.max_afstand_vlak_oppwater = 2
        self.max_afstand_pand_oppwater = 6
        self.max_afstand_vlak_kolk = 30
        self.max_afstand_afgekoppeld = 3
        self.max_afstand_drievoudig = 4
        self.afkoppelen_hellende_daken = True
        self.bouwjaar_gescheiden_binnenhuisriolering = 1992
        self.verhardingsgraad_erf = 50
        self.verhardingsgraad_half_verhard = 50

    def from_file(self):
        pass

    def to_file(self):
        pass


class BGTInloopTool:

    def __init__(self, parameters: InputParameters):
        """Constructor."""
        self.parameters = parameters
        self.database = Database()

    def calculate_runoff_targets(self):

        bgt_surfaces = self.database.bgt_surfaces
        result_table = self.database.result_table
        feature_defn = result_table.GetLayerDefn()

        for surface in bgt_surfaces:
            feature = ogr.Feature(feature_defn)
            afwatering = self.decision_tree(surface, self.parameters)
            # feature.SetField(RESULT_TABLE_FIELD_ID, val) --> is autoincrement field
            feature.SetField(RESULT_TABLE_FIELD_LAATSTE_WIJZIGING, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            feature.SetField(RESULT_TABLE_FIELD_BGT_IDENTIFICATIE, surface.identificatie_lokaalid)
            # feature.SetField(RESULT_TABLE_FIELD_TYPE_VERHARDING, val)
            # feature.SetField(RESULT_TABLE_FIELD_GRAAD_VERHARDING, val)
            # feature.SetField(RESULT_TABLE_FIELD_HELLINGSTYPE, val)
            # feature.SetField(RESULT_TABLE_FIELD_HELLINGSPERCENTAGE, val)
            # feature.SetField(RESULT_TABLE_FIELD_BERGING_DAK, val)
            # feature.SetField(RESULT_TABLE_FIELD_PUTCODE, val)
            # feature.SetField(RESULT_TABLE_FIELD_LEIDINGCODE, val)
            feature.SetField(TARGET_TYPE_GEMENGD_RIOOL, afwatering[TARGET_TYPE_GEMENGD_RIOOL])
            feature.SetField(TARGET_TYPE_HEMELWATERRIOOL, afwatering[TARGET_TYPE_HEMELWATERRIOOL])
            feature.SetField(TARGET_TYPE_VGS_HEMELWATERRIOOL, afwatering[TARGET_TYPE_VGS_HEMELWATERRIOOL])
            feature.SetField(TARGET_TYPE_INFILTRATIEVOORZIENING, afwatering[TARGET_TYPE_INFILTRATIEVOORZIENING])
            feature.SetField(TARGET_TYPE_NIET_AANGESLOTEN, afwatering[TARGET_TYPE_NIET_AANGESLOTEN])
            result_table.CreateFeature(feature)
            feature = None

    def decision_tree(self, surface, parameters):
        result = {
            TARGET_TYPE_GEMENGD_RIOOL: 0,
            TARGET_TYPE_HEMELWATERRIOOL: 0,
            TARGET_TYPE_VGS_HEMELWATERRIOOL: 0,
            TARGET_TYPE_INFILTRATIEVOORZIENING: 0,
            TARGET_TYPE_NIET_AANGESLOTEN: 0
        }
        
        if surface.surface_type in NON_CONNECTABLE_SURFACE_TYPES:
            result[TARGET_TYPE_NIET_AANGESLOTEN] = 100

        elif not any(
                [
                    surface.distance_hemelwaterriool,
                    surface.distance_vuilwaterriool,
                    surface.distance_infiltratievoorziening,
                    surface.distance_gemengd_riool,
                    surface.distance_oppervlaktewater,
                ]
        ):
            result[TARGET_TYPE_NIET_AANGESLOTEN] = 100

        elif surface.surface_type == SURFACE_TYPE_PAND:
            pass

        elif surface.fysiek_voorkomen == FYSIEK_VOORKOMEN_VERHARD:

            if surface.distance_oppervlaktewater or np.inf < parameters.max_afstand_vlak_oppwater:
                result[TARGET_TYPE_NIET_AANGESLOTEN] = 100

            elif (
                    surface.distance_gemengd_riool
                    or np.inf - min(surface.distance_hemelwaterriool or np.inf,
                                    surface.distance_infiltratievoorziening or np.inf)
                    < parameters.max_afstand_afgekoppeld
            ):

                if surface.distance_hemelwaterriool or np.inf < surface.distance_infiltratievoorziening or np.inf:
                    result[TARGET_TYPE_HEMELWATERRIOOL] = 100
                else:
                    result[TARGET_TYPE_INFILTRATIEVOORZIENING] = 100

            elif (
                    surface.distance_gemengd_riool
                    or np.inf - min(surface.distance_hemelwaterriool or np.inf,
                                    surface.distance_infiltratievoorziening or np.inf)
                    > parameters.max_afstand_afgekoppeld
            ):

                if surface.distance_gemengd_riool or np.inf < min(
                        surface.distance_hemelwaterriool or np.inf, surface.distance_infiltratievoorziening or np.inf
                ):
                    result[TARGET_TYPE_GEMENGD_RIOOL] = 100

                elif surface.distance_hemelwaterriool or np.inf < surface.distance_infiltratievoorziening or np.inf:
                    result[TARGET_TYPE_HEMELWATERRIOOL] = 100

                else:
                    result[TARGET_TYPE_INFILTRATIEVOORZIENING] = 100

        else:
            pass

        return result

class DatabaseOperationError(Exception):
    """Raised when an invalid database operation is requested"""
    pass

class Database:

    def __init__(self):
        self.mem_database = GPKG_DRIVER.CreateDataSource('/vsimem/database.gpkg')
        self.empty_result_table()
        self._sql_dir = SQL_DIR

    def empty_result_table(self):
        """Create or replace the result table"""
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(28992)

        lyr = self.mem_database.CreateLayer('bgt_inlooptabel',
                                            srs,
                                            geom_type=schema.GEOMETRY_TYPE,
                                            options=['FID={}'.format(schema.PRIMARY_KEY)]
                                            )  # spatial index is added by default

        for fieldname, datatype in schema.FIELDS.items():
            field_defn = ogr.FieldDefn(fieldname, datatype)
            lyr.CreateField(field_defn)

        lyr = None

    @property
    def result_table(self):
        return self.mem_database.GetLayerByName('bgt_inlooptabel')

    @property
    def bgt_surfaces(self):
        return self.mem_database.GetLayerByName('bgt_surfaces')

    def import_pipes(self, datasource):
        lines_gpkg = ogr.Open(datasource)
        self.mem_database.CopyLayer(lines_gpkg.GetLayerByName("default_lijn"), "pipes")

    def import_surfaces(self, bgt_zip_file):

        dest_srs = osr.SpatialReference()
        dest_srs.ImportFromEPSG(28992)
        dest_layer = self.mem_database.CreateLayer(
            DB_TABEL_BGT_OPPERVLAK, dest_srs, 3, ["OVERWRITE=YES", "GEOMETRY_NAME=geom"]
        )

        # adding fields to new layer
        add_text_fields = ["identificatie_lokaalid", "surface_type", "bgt_fysiek_voorkomen"]

        for field in add_text_fields:
            field_name = ogr.FieldDefn(field, ogr.OFTString)
            field_name.SetWidth(60)
            dest_layer.CreateField(field_name)

        add_real_fields = [
            "distance_oppervlaktewater",
            "distance_hemelwaterriool",
            "distance_vuilwaterriool",
            "distance_infiltratievoorziening",
            "distance_gemengd_riool",
        ]

        for field in add_real_fields:
            field_name = ogr.FieldDefn(field, ogr.OFTReal)
            field_name.SetWidth(20)
            dest_layer.CreateField(field_name)

        for surface in ALL_USED_SURFACE_TYPES:

            print(surface)
            bgt_zip_file_abspath = os.path.abspath(bgt_zip_file)
            if not os.path.isfile(bgt_zip_file_abspath):
                raise FileNotFoundError('BGT zip niet gevonden: {}'.format(bgt_zip_file_abspath))
            surface_source_fn = os.path.join("/vsizip/" + bgt_zip_file, f"bgt_{surface}.gml")
            print(surface_source_fn)
            surface_source = ogr.Open(surface_source_fn)
            input_layer = surface_source.GetLayerByName(f"{surface}")

            # TODO import versnellen

            for i in range(0, input_layer.GetFeatureCount()):
                feature = input_layer.GetFeature(i)

                if feature:

                    if feature["eindRegistratie"] is None:
                        if hasattr(feature, 'plus-status'):
                            if feature['plus-status'] in ['plan', 'historie']:
                                continue
                        new_feature = ogr.Feature(dest_layer.GetLayerDefn())
                        new_feature.SetField("identificatie_lokaalid", feature["identificatie.lokaalID"])
                        new_feature.SetField("surface_type", f"{surface}")

                        if surface in SURFACE_TYPES_MET_FYSIEK_VOORKOMEN:
                            new_feature["bgt_fysiek_voorkomen"] = feature["bgt-fysiekVoorkomen"]

                        target_geometry = ogr.ForceToPolygon(feature.geometry())
                        target_geometry.AssignSpatialReference(dest_srs)
                        new_feature.SetGeometry(target_geometry)
                        dest_layer.CreateFeature(new_feature)

                        target_geometry = None
                        new_feature = None

            surface_source = None
            input_layer = None

        dest_layer = None

    def import_buildings(self, datasource, field_map):
        pass

    def clean_surfaces(self):
        pass

    def classify_surfaces(self, parameters):
        """Bepaal NWRW vlaktype van alle geïmporteerde oppervlakken"""
        layer = self.mem_database.GetLayerByName(DB_TABEL_BGT_OPPERVLAK)
        if layer is None:
            raise DatabaseOperationError
        # add fields if not exists
        for field_name in [RESULT_TABLE_FIELD_TYPE_VERHARDING, RESULT_TABLE_FIELD_GRAAD_VERHARDING]:
            if layer.FindFieldIndex(field_name, 1) == -1:
                field_defn = ogr.FieldDefn(field_name, ogr.OFTString)
                field_defn.SetWidth(60)
                layer.CreateField(field_defn)
        for feature in layer:
            if feature.surface_type == SURFACE_TYPE_PAND:
                verhardingstype = VERHARDINGSTYPE_PAND
            elif feature.surface_type == SURFACE_TYPE_WATERDEEL:
                verhardingstype = VERHARDINGSTYPE_WATER
            elif feature.surface_type == SURFACE_TYPE_ONDERSTEUNENDWATERDEEL:
                verhardingstype = VERHARDINGSTYPE_ONVERHARD
            elif feature.surface_type in SURFACE_TYPES_MET_FYSIEK_VOORKOMEN:
                if feature.bgt_fysiek_voorkomen in ('loofbos', 'heide', 'gemengd bos', 'groenvoorziening', 'transitie',
                                                    'rietland', 'grasland overig', 'houtwal', 'zand', 'moeras',
                                                    'fruitteelt', 'naaldbos', 'struiken', 'bouwland', 'duin',
                                                    'boomteelt', 'grasland agrarisch', 'onverhard', 'kwelder'):
                    verhardingstype = VERHARDINGSTYPE_ONVERHARD
                elif feature.bgt_fysiek_voorkomen == 'open verharding':
                    verhardingstype = VERHARDINGSTYPE_OPEN_VERHARD
                elif feature.bgt_fysiek_voorkomen == 'half verhard':
                    verhardingstype = VERHARDINGSTYPE_OPEN_VERHARD
                    verhardingsgraad = parameters.verhardingsgraad_half_verhard
                elif feature.bgt_fysiek_voorkomen == 'erf':
                    verhardingstype = VERHARDINGSTYPE_OPEN_VERHARD
                    verhardingsgraad = parameters.verhardingsgraad_erf
                elif feature.bgt_fysiek_voorkomen == 'gesloten verhard':
                    verhardingstype = VERHARDINGSTYPE_GESLOTEN_VERHARD

        feature[RESULT_TABLE_FIELD_TYPE_VERHARDING] = verhardingstype
        feature[RESULT_TABLE_FIELD_GRAAD_VERHARDING] = verhardingsgraad

    def add_build_year_to_surface(self):
        pass

    def calculate_distances(self, parameters):

        calculate_distance_pipe_sql = f"""SELECT    surface.gml_id, 
                                                    pipe."Naam" AS leiding_naam, 
                                                    pipe."TypeNaam" AS leiding_typenaam, 
                                                    ST_Distance(pipe.geom, surface.geom) AS distance 
                                           FROM     pipes as pipe, 
                                                    bgt_surfaces AS surface 
                                           WHERE    PtDistWithin(
                                                        pipe.geom, 
                                                        surface.geom, 
                                                        {parameters.max_afstand_vlak_afwateringsvoorziening}
                                                    )
                                           GROUP BY surface.gml_id, 
                                                    pipe."TypeNaam" 
                                           ORDER BY surface.gml_id, 
                                                    ST_Distance(pipe.geom, surface.geom) ASC
                                           ;
                                        """

        pipe_distance_layer = self.mem_database.ExecuteSQL(calculate_distance_pipe_sql)
        new_layer = self.mem_database.CopyLayer(pipe_distance_layer, "pipe_distances")
        new_layer = None

        calculate_distance_oppervlaktewater_sql = f""" SELECT  surface1.gml_id AS gml_id, 
                                                    ST_Distance(surface1.geom, surface2.geom) AS distance
                                            FROM    bgt_surfaces AS surface1, 
                                                    bgt_surfaces as surface2
                                            WHERE   surface1.surface_type != '{SURFACE_TYPE_WATERDEEL}' 
                                                    AND surface2.surface_type = {SURFACE_TYPE_WATERDEEL}
                                            AND     PtDistWithin(
                                                        surface1.geom, 
                                                        surface2.geom, 
                                                        {parameters.max_afstand_vlak_afwateringsvoorziening}
                                                        )
                                            GROUP BY surface1.gml_id 
                                            ORDER BY ST_Distance(surface1.geom, surface2.geom) ASC
                                            ;
                                        """

        water_distance_layer = self.mem_database.ExecuteSQL(
            calculate_distance_oppervlaktewater_sql
        )
        new_layer = self.mem_database.CopyLayer(water_distance_layer, "water_distances")
        new_layer = None

        # Update water distances
        update_water_distances = os.path.join(SQL_DIR, "update_water_distances.sql")
        with open(update_water_distances, "r") as file:
            update_water_distances_sql = file.read()
        self.mem_database.ExecuteSQL(update_water_distances_sql)

        # Udpate pipe distances
        update_pipe_distances = os.path.join(SQL_DIR, "update_pipe_distances.sql")
        with open(update_pipe_distances, "r") as file:
            update_pipe_distances_sql = file.read()
        self.mem_database.ExecuteSQL(update_pipe_distances_sql)
