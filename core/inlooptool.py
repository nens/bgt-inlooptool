
# system imports
import os

# Third-party imports 
import osr
import numpy as np
from osgeo import ogr
from osgeo import gdal
from datetime import datetime
from tqdm import tqdm

# Local imports
from core import result_table_schema as schema
from core.constants import *
from core.constants import (
         ALL_USED_SURFACE_TYPES,
         DB_TABEL_BGT_OPPERVLAK,
         RESULT_TABLE_FIELD_GRAAD_VERHARDING,
         RESULT_TABLE_FIELD_TYPE_VERHARDING,
         SURFACE_TYPE_PAND,
         VERHARDINGSTYPE_PAND,
         SURFACE_TYPE_WATERDEEL,
         VERHARDINGSTYPE_WATER
         
         )

# Globals 
SQL_DIR = os.path.join(__file__, 'sql')

# Exceptions
gdal.UseExceptions()

# Drivers
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

    def __init__(self, epsg=28992):        
        self.srs = osr.SpatialReference()
        self.srs.ImportFromEPSG(epsg)
        self.epsg = epsg

        self.mem_database = GPKG_DRIVER.CreateDataSource('/vsimem/database.gpkg')
        self.empty_result_table()
        self._sql_dir = SQL_DIR
        
    def import_surfaces(self, extract_path):
        
        self.load_surfaces(extract_path)
        self.clean_surfaces()
        self.register_epsg()
        self.register_surfaces()
        self.merge_surfaces()

    def empty_result_table(self):
        """Create or replace the result table"""
        lyr = self.mem_database.CreateLayer('bgt_inlooptabel',
                                            self.srs,
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
        return self.mem_database.GetLayerByName('bgt_oppervlak')

    def import_pipes(self, datasource):
        lines_gpkg = ogr.Open(datasource)
        self.mem_database.CopyLayer(lines_gpkg.GetLayerByName("default_lijn"), "pipes")
   
    def import_buildings(self, datasource, field_map):
        pass

    def classify_surfaces(self, parameters):
        """Bepaal NWRW vlaktype van alle geïmporteerde oppervlakken"""
        layer = self.bgt_surfaces 
        if layer is None:
            raise DatabaseOperationError
        # add fields if not exists
        for field_name in [RESULT_TABLE_FIELD_TYPE_VERHARDING, RESULT_TABLE_FIELD_GRAAD_VERHARDING]:
            if layer.FindFieldIndex(field_name, 1) == -1:
                field_defn = ogr.FieldDefn(field_name, ogr.OFTString)
                field_defn.SetWidth(60)
                layer.CreateField(field_defn)
                
        for feature in layer:
            if feature:
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
                layer.SetFeature(feature)
        layer = None
            
        
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
        
    def merge_surfaces(self):
        """ merging and standardizing all surfaces to one layer"""
        dest_layer = self.mem_database.CreateLayer(
            DB_TABEL_BGT_OPPERVLAK, self.srs, 3, 
            ["OVERWRITE=YES", "GEOMETRY_NAME=geom"]
        )

        # adding fields to new layer
        add_text_fields = ["identificatie_lokaalid", 
                           "surface_type",
                           "bgt_fysiek_voorkomen"]

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
            input_layer = self.mem_database.GetLayerByName(f"{surface}")

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
                        target_geometry.AssignSpatialReference(self.srs)
                        new_feature.SetGeometry(target_geometry)
                        dest_layer.CreateFeature(new_feature)

                        target_geometry = None
                        new_feature = None
        dest_layer = None
        
    def load_surfaces(self, bgt_zip_file:str):
        """ returns a bgt loaded geopackage"""
        bgt_zip_file_abspath = os.path.abspath(bgt_zip_file)
        if not os.path.isfile(bgt_zip_file_abspath):
            raise FileNotFoundError('BGT zip niet gevonden: {}'.format(bgt_zip_file_abspath))

        for stype in ALL_USED_SURFACE_TYPES:
            surface_source_fn = os.path.join("/vsizip/" + bgt_zip_file, 
                                             f"bgt_{stype}.gml")
            surface_source = ogr.Open(surface_source_fn)
            src_layer = surface_source.GetLayerByName(f"{stype}")
            self.mem_database.CopyLayer(src_layer=src_layer, new_name=stype)
    
    def clean_surfaces(self):
        """ returns an updated geopackage with no linestrings/multipolygons/multisurfaces/curved polygons"""
        for stype in ALL_USED_SURFACE_TYPES:
            #print('Cleaning up {}'.format(stype))
            lyr = self.mem_database.GetLayerByName(stype)
            lyr.StartTransaction()
            for f in lyr:
                geom=f.GetGeometryRef()
                geom_type = geom.GetGeometryType()
                if geom_type == ogr.wkbPolygon:
                    pass
                elif geom_type == ogr.wkbCurvePolygon:
                    #print('Fixing Curve Polygon feature {}'.format(f.GetFID()))
                    geom_linear = geom.GetLinearGeometry()
                    f.SetGeometry(geom_linear)
                    lyr.SetFeature(f)
                elif geom_type in [ogr.wkbMultiSurface, ogr.wkbMultiPolygon]:
                    #print('Fixing MultiSurface or MultiPolygon feature {}'.format(f.GetFID()))
                    geom_fixed = ogr.ForceToPolygon(geom)
                    f.SetGeometry(geom_fixed)
                    lyr.SetFeature(f)
                elif geom_type in (ogr.wkbLineString, ogr.wkbCompoundCurve):
                    #print('Deleting feature {} because it is a Linestring'.format(f.GetFID()))
                    lyr.DeleteFeature(f.GetFID())
                else:
                    #print('Fixing feature {} failed!'.format(f.GetFID()))
                    raise Exception('No procedure defined to clean up geometry type {}'.format(str(geom_type)))
        
            lyr.CommitTransaction()    
            lyr = None
       
    def register_epsg(self):
        """gpkg must have been opened with update=1
        Only registers srs if no row of that id exists in gpkg_spatial_ref_sys"""
        if self.srs.IsProjected():
            cstype='PROJCS'
        elif self.srs.IsGeographic():
            cstype='GEOGCS'
        else:
            raise ValueError('Invalid SRS')

        sql = """SELECT * FROM gpkg_spatial_ref_sys WHERE srs_id = {}""".format(
            self.srs.GetAuthorityCode(cstype))
        result_lyr = self.mem_database.ExecuteSQL(sql)
        result_row_count = result_lyr.GetFeatureCount()
        self.mem_database.ReleaseResultSet(result_lyr)
        if result_row_count == 0:
            sql =   """
                    INSERT INTO gpkg_spatial_ref_sys (
                      srs_name,
                      srs_id,
                      organization,
                      organization_coordsys_id,
                      definition,
                      description
                    )
                    VALUES (
                        '{srs_name}',
                        {srs_id},
                        '{organization}',
                        {organization_coordsys_id},
                        '{definition}',
                        '{description}'
                    );
                    """.format(
                        srs_name=self.srs.GetAttrValue(cstype),
                        srs_id=self.srs.GetAuthorityCode(cstype),
                        organization=self.srs.GetAuthorityName(cstype),
                        organization_coordsys_id=self.srs.GetAuthorityCode(cstype),
                        definition=self.srs.ExportToWkt(),
                        description=self.srs.GetAttrValue(cstype)
                    )
            self.mem_database.ExecuteSQL(sql)
    
    def register_surfaces(self):
        """register tables in gpkg geometry admin tables"""
        for stype in ALL_USED_SURFACE_TYPES:
            lyr = self.mem_database.GetLayerByName(stype)
            x0, x1, y0, y1 = lyr.GetExtent()
            sql = """DELETE FROM gpkg_contents WHERE table_name = '{}';""".format(stype)
            self.mem_database.ExecuteSQL(sql)
            sql =   """
                    INSERT INTO gpkg_contents (
                        table_name,
                        data_type,
                        identifier,
                        description,
                        min_x, max_x, min_y, max_y,
                        srs_id
                    )
                    VALUES ('{table_name}', '{data_type}', '{identifier}', '{description}',
                            {min_x}, {max_x}, {min_y}, {max_y}, {srs_id});
                    """.format(
                        table_name = stype,
                        data_type='features',
                        identifier=stype,
                        description=stype,
                        min_x=x0,
                        max_x=x1,
                        min_y=y0,
                        max_y=y1,
                        srs_id=self.epsg
                    )
            self.mem_database.ExecuteSQL(sql)
            sql = """DELETE FROM gpkg_geometry_columns WHERE table_name = '{}';""".format(stype)
            self.mem_database.ExecuteSQL(sql)
            sql =   """
                    INSERT INTO gpkg_geometry_columns (table_name, column_name, geometry_type_name, srs_id, z, m)
                    VALUES ('{table_name}','{column_name}','{geometry_type_name}',{srs_id},{z},{m});
                    """.format(
                        table_name=stype,
                        column_name='geom',
                        geometry_type_name='POLYGON',
                        srs_id=28992,
                        z=0,
                        m=0
                    )
            self.mem_database.ExecuteSQL(sql)   
        

if __name__ == "__main__":
    pass
    path = 'C:/Users/chris.kerklaan/Documents/Github/bgt-inlooptool/test-data/extract/bgt_{}.gml'.format(stype)
    # test
    ds = ogr.Open(out_gpkg_fn, update=1)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(28992)
    gpkg_register_crs(ds, srs)
    ds = None
       

out_gpkg_fn = 'C:/Users/chris.kerklaan/Documents/Github/bgt-inlooptool/leeg.gpkg'

