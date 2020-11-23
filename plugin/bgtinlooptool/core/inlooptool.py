# System imports
import os

# Third-party imports
import osr
import numpy as np
from osgeo import ogr
from osgeo import gdal
from datetime import datetime

try:
    import rtree

    USE_INDEX = True
except ImportError:
    USE_INDEX = False

# Local imports
from core import result_table_schema as schema
from core.constants import *
from core.constants import (
    ALL_USED_SURFACE_TYPES,
    SURFACES_TABLE_NAME,
    RESULT_TABLE_FIELD_GRAAD_VERHARDING,
    RESULT_TABLE_FIELD_TYPE_VERHARDING,
    SURFACE_TYPE_PAND,
    VERHARDINGSTYPE_PAND,
    SURFACE_TYPE_WATERDEEL,
    VERHARDINGSTYPE_WATER,
    DISTANCE_TYPE_NAAM,
    PIPES_TABLE_NAME,
)
from core.defaults import *

# Globals
SQL_DIR = os.path.join(__file__, "sql")

# Exceptions
gdal.UseExceptions()


class DatabaseOperationError(Exception):
    """Raised when an invalid _database operation is requested"""

    pass


class FileInputError(Exception):
    """Raised when an attempt is made to import an invalid file"""

    pass


# Drivers
GPKG_DRIVER = ogr.GetDriverByName("GPKG")


class InputParameters:
    """Parameters that determine the behaviour of the tool"""

    def __init__(self,
                 max_afstand_vlak_afwateringsvoorziening=MAX_AFSTAND_VLAK_AFWATERINGSVOORZIENING,
                 max_afstand_vlak_oppwater=MAX_AFSTAND_VLAK_OPPWATER,
                 max_afstand_pand_oppwater=MAX_AFSTAND_PAND_OPPWATER,
                 max_afstand_vlak_kolk=MAX_AFSTAND_VLAK_KOLK,
                 max_afstand_afgekoppeld=MAX_AFSTAND_AFGEKOPPELD,
                 max_afstand_drievoudig=MAX_AFSTAND_DRIEVOUDIG,
                 afkoppelen_hellende_daken=AFKOPPELEN_HELLENDE_DAKEN,
                 bouwjaar_gescheiden_binnenhuisriolering=BOUWJAAR_GESCHEIDEN_BINNENHUISRIOLERING,
                 verhardingsgraad_erf=VERHARDINGSGRAAD_ERF,
                 verhardingsgraad_half_verhard=VERHARDINGSGRAAD_HALF_VERHARD):
        self.max_afstand_vlak_afwateringsvoorziening = (max_afstand_vlak_afwateringsvoorziening)
        self.max_afstand_vlak_oppwater = max_afstand_vlak_oppwater
        self.max_afstand_pand_oppwater = max_afstand_pand_oppwater
        self.max_afstand_vlak_kolk = max_afstand_vlak_kolk
        self.max_afstand_afgekoppeld = max_afstand_afgekoppeld
        self.max_afstand_drievoudig = max_afstand_drievoudig
        self.afkoppelen_hellende_daken = afkoppelen_hellende_daken
        self.bouwjaar_gescheiden_binnenhuisriolering = (bouwjaar_gescheiden_binnenhuisriolering)
        self.verhardingsgraad_erf = verhardingsgraad_erf
        self.verhardingsgraad_half_verhard = verhardingsgraad_half_verhard

    def from_file(self):
        pass

    def to_file(self):
        pass


class InloopTool:
    def __init__(self, parameters):
        """Constructor."""
        self.parameters = parameters
        self._database = Database()

    def import_surfaces(self, file_path):
        """
        Import BGT Surfaces to _database
        :param file_path: path to bgt zip file
        :return: None
        """
        self._database.import_surfaces_raw(file_path)
        self._database.clean_surfaces()
        self._database.register_epsg()
        self._database.register_surfaces()
        self._database.merge_surfaces()
        self._database.classify_surfaces(self.parameters)

    def import_pipes(self, file_path):
        """
        Import pipes to database
        :param file_path: path to GWSW Geopackage that contains the pipes
        :return: None
        """
        self._database.import_pipes(file_path=file_path)

    def import_buildings(self, file_path):
        """
        Import buildings to database
        :param file_path: path to GWSW Geopackage that contains the pipes
        :return: None
        """
        self._database.import_buildings(file_path=file_path)

    def decision_tree(self, surface, parameters):
        """
        Determine target percentages for one surface
        :param surface:
        :param parameters:
        :return: dict with percentages per target type
        :rtype dict
        """
        result = {
            TARGET_TYPE_GEMENGD_RIOOL: 0,
            TARGET_TYPE_HEMELWATERRIOOL: 0,
            TARGET_TYPE_VGS_HEMELWATERRIOOL: 0,
            TARGET_TYPE_INFILTRATIEVOORZIENING: 0,
            TARGET_TYPE_NIET_AANGESLOTEN: 0,
        }

        def verhard():
            """Is het oppervlak (mogelijk/deels) verhard?"""
            if surface.surface_type in NON_CONNECTABLE_SURFACE_TYPES:
                return False
            elif surface.type_verharding in FYSIEK_VOORKOMEN_VERHARD:
                return True
            else:
                return False

        def bij_hov():
            """Ligt het oppervlak dichtbij een hemelwaterontvangende voorziening?"""
            return min(surface.distance_hemelwaterriool,
                       surface.distance_vuilwaterriool,
                       surface.distance_infiltratievoorziening,
                       surface.distance_gemengd_riool,
                       surface.distance_oppervlaktewater) != 9999

        def is_bouwwerk():
            return surface.surface_type in [SURFACE_TYPE_PAND, SURFACE_TYPE_GEBOUWINSTALLATIE]

        def bij_water():
            return surface.distance_oppervlaktewater < parameters.max_afstand_vlak_oppwater

        def bij_kolk():
            return True

        def bij_gem_plus_hwa():
            """Ligt het oppervlak in de buurt van een straat waar naast gemengd ook rwa is gelegd?"""
            
            if surface.distance_gemengd_riool != 9999 and (surface.distance_hemelwaterriool != 9999 or surface.distance_infiltratievoorziening != 9999):            
                return abs(surface.distance_gemengd_riool
                           -
                           min(surface.distance_hemelwaterriool,
                               surface.distance_infiltratievoorziening)) <= parameters.max_afstand_afgekoppeld
            else:
                return False

        def gem_dichtst_bij():
            """Ligt het gemengde riool dichterbij dan HWA/VGS-HWA/Infiltratieriool?"""
            return surface.distance_gemengd_riool < min(surface.distance_hemelwaterriool,
                                                        surface.distance_infiltratievoorziening)

        def hwa_dichterbij_dan_hwavgs_en_infiltr():
            """Ligt het HWA riool dichterbij dan het infiltratieriool?"""
            return surface.distance_hemelwaterriool < surface.distance_infiltratievoorziening
            
        def bij_drievoudig_stelsel_crit1():
            return False

        def bij_drievoudig_stelsel_crit2():
            return False

        def bij_drievoudig_stelsel_crit3():
            return False

        def hwa_vgs_dichterbij_dan_infiltr():
            return False

        def nieuw_pand():
            """Is het bouwjaar van het pand later dan de ondergrens voor gescheiden binnenhuis riolering?"""
            if surface.build_year is None:
                return False
            else:
                return surface.build_year > parameters.bouwjaar_gescheiden_binnenhuisriolering

        def hellend_dak():
            return True

        for distance in ['distance_gemengd_riool', 'distance_hemelwaterriool', 'distance_vuilwaterriool',
                         'distance_infiltratievoorziening', 'distance_oppervlaktewater']:
            if surface[distance] is None:
                surface[distance] = 9999

        if not verhard():
            result[TARGET_TYPE_NIET_AANGESLOTEN] = 100

        elif not bij_hov():
            result[TARGET_TYPE_NIET_AANGESLOTEN] = 100

        # PANDEN
        elif is_bouwwerk():
            if bij_water():
                result[TARGET_TYPE_NIET_AANGESLOTEN] = 100
            
            elif bij_gem_plus_hwa():
                if self.parameters.afkoppelen_hellende_daken:
                    if nieuw_pand() and hellend_dak():
                        if bij_drievoudig_stelsel_crit1():
                            if bij_drievoudig_stelsel_crit2():
                                result[TARGET_TYPE_INFILTRATIEVOORZIENING] = 50
                                result[TARGET_TYPE_GEMENGD_RIOOL] = 50
                            else:
                                result[TARGET_TYPE_HEMELWATERRIOOL] = 50
                                result[TARGET_TYPE_GEMENGD_RIOOL] = 50
                        else:
                            if hwa_dichterbij_dan_hwavgs_en_infiltr():
                                result[TARGET_TYPE_HEMELWATERRIOOL] = 50
                                result[TARGET_TYPE_GEMENGD_RIOOL] = 50
                            else:
                                if hwa_vgs_dichterbij_dan_infiltr():
                                    result[TARGET_TYPE_VGS_HEMELWATERRIOOL] = 50
                                    result[TARGET_TYPE_GEMENGD_RIOOL] = 50
                                else:
                                    result[TARGET_TYPE_INFILTRATIEVOORZIENING] = 50
                                    result[TARGET_TYPE_GEMENGD_RIOOL] = 50
                    
                    else:
                        if gem_dichtst_bij():
                            result[TARGET_TYPE_GEMENGD_RIOOL] = 100
                        elif hwa_dichterbij_dan_hwavgs_en_infiltr():
                            result[TARGET_TYPE_HEMELWATERRIOOL] = 100
                        else:
                            result[TARGET_TYPE_INFILTRATIEVOORZIENING] = 100
                else:
                    result[TARGET_TYPE_GEMENGD_RIOOL] = 100
            else:
                if gem_dichtst_bij():
                    result[TARGET_TYPE_GEMENGD_RIOOL] = 100
                elif bij_drievoudig_stelsel_crit1():
                    if bij_drievoudig_stelsel_crit2():
                        result[TARGET_TYPE_INFILTRATIEVOORZIENING] = 100
                    else:
                        result[TARGET_TYPE_HEMELWATERRIOOL] = 100
                else:
                    if hwa_dichterbij_dan_hwavgs_en_infiltr():
                        result[TARGET_TYPE_HEMELWATERRIOOL] = 100
                    else:
                        if hwa_vgs_dichterbij_dan_infiltr():
                            pass
                        elif surface.distance_infiltratievoorziening != 9999:
                            result[TARGET_TYPE_INFILTRATIEVOORZIENING] = 100
                        else:
                            result[TARGET_TYPE_NIET_AANGESLOTEN] = 100

        # Overige verharde oppervlakken
        elif verhard():
            if bij_water():
                result[TARGET_TYPE_NIET_AANGESLOTEN] = 100
            else:
                if bij_kolk():
                    if (not bij_gem_plus_hwa()) and gem_dichtst_bij():
                        result[TARGET_TYPE_GEMENGD_RIOOL] = 100
                    else:
                        if bij_drievoudig_stelsel_crit1():
                            if bij_drievoudig_stelsel_crit3():
                                result[TARGET_TYPE_VGS_HEMELWATERRIOOL] = 100
                            else:
                                result[TARGET_TYPE_HEMELWATERRIOOL] = 100
                        if hwa_dichterbij_dan_hwavgs_en_infiltr():
                            result[TARGET_TYPE_HEMELWATERRIOOL] = 100
                        else:
                            if hwa_vgs_dichterbij_dan_infiltr():
                                result[TARGET_TYPE_VGS_HEMELWATERRIOOL] = 100
                            elif surface.distance_infiltratievoorziening != 9999:
                                result[TARGET_TYPE_INFILTRATIEVOORZIENING] = 100
                            else:
                                result[TARGET_TYPE_NIET_AANGESLOTEN] = 100                                
                else:
                    result[TARGET_TYPE_NIET_AANGESLOTEN] = 100
        return result

    def calculate_distances(self, parameters, use_index=USE_INDEX):
        """
        For all BGT Surfaces, calculate the distance to the nearest pipe of each type and nearest surface water
        :param parameters: input parameters
        :return: None
        """

        surfaces = self._database.mem_database.GetLayerByName(SURFACES_TABLE_NAME)
        pipes = self._database.mem_database.GetLayerByName(PIPES_TABLE_NAME)

        if use_index:
            surface_idx = create_index(surfaces)
            pipe_idx = create_index(pipes)

        out_layer = Layer(
            self._database.mem_database.CreateLayer(
                "pipe_distances",
                self._database.srs,
                surfaces.GetGeomType(),
                ["OVERWRITE=TRUE"],
            )
        )

        out_layer.add_field("surface_lokaalid", ogr.OFTString)
        for field in list(set(DISTANCE_TYPE_NAAM.values())):
            out_layer.add_field("distance_" + field, ogr.OFTReal)
            out_layer.add_field("naam_" + field, ogr.OFTReal)

        lokaalid_distances = {}
        surfaces.ResetReading()
        surfaces.SetSpatialFilter(None)
        for surface_id in range(0, surfaces.GetFeatureCount()):
            surface = surfaces.GetFeature(surface_id)

            if not surface:
                continue

            surface_geom = surface.geometry()
            buffered = surface_geom.Buffer(
                parameters.max_afstand_vlak_afwateringsvoorziening
            )

            distances = []
            pipe_ids = []
            pipe_types = []
            if use_index:
                for pipe_id in pipe_idx.intersection(buffered.GetEnvelope()):
                    pipe = pipes.GetFeature(pipe_id)
                    pipe_geom = pipe.geometry()
                    if pipe_geom.Intersects(buffered):
                        distances.append(pipe_geom.Distance(surface_geom))
                        pipe_ids.append(pipe.GetFID())
                        pipe_types.append(pipe["TypeNaam"])

            else:
                pipes.SetSpatialFilter(buffered)
                for pipe in pipes:
                    pipe_geom = pipe.geometry()
                    if pipe_geom.Intersects(buffered):
                        distances.append(pipe_geom.Distance(surface_geom))
                        pipe_ids.append(pipe.GetFID())
                        pipe_types.append(pipe["TypeNaam"])

            if len(distances) == 0:
                continue
            else:
                lokaalid = surface["identificatie_lokaalid"]
                pipe_dict = {"surface_lokaalid": lokaalid}
                pipe_types_unique = [
                    p for p in set(pipe_types) if p in DISTANCE_TYPE_NAAM
                ]
                for pipe_type in pipe_types_unique:
                    min_dist = min(
                        [
                            distances[i]
                            for i, v in enumerate(pipe_types)
                            if v == pipe_type
                        ]
                    )
                    pipe_id = pipe_ids[distances.index(min_dist)]
                    pipe = pipes.GetFeature(pipe_id)
                    name = DISTANCE_TYPE_NAAM[pipe_type]
                    pipe_dict.update(
                        {"distance_" + name: min_dist, "naam_" + name: pipe["Naam"]}
                    )
                out_layer.add_feature(surface_geom, pipe_dict)

            del pipe_dict["surface_lokaalid"]
            lokaalid_distances[lokaalid] = pipe_dict

        pipes.SetSpatialFilter(None)
        out_layer.layer = None
        pipes = None

        out_layer = Layer(
            self._database.mem_database.CreateLayer(
                "water_distances",
                self._database.srs,
                surfaces.GetGeomType(),
                ["OVERWRITE=TRUE"],
            )
        )

        out_layer.add_field("surface_lokaalid", ogr.OFTString)
        out_layer.add_field("distance", ogr.OFTReal)

        surfaces.SetSpatialFilter(None)
        surfaces.ResetReading()
        for surface_id in range(0, surfaces.GetFeatureCount()):
            surface = surfaces.GetFeature(surface_id)

            if not surface:
                continue

            if surface.surface_type == SURFACE_TYPE_WATERDEEL:
                continue

            surface_geom = surface.geometry().Clone()
            buffered = surface_geom.Buffer(
                parameters.max_afstand_vlak_afwateringsvoorziening
            )
            surface_id_or = surface["identificatie_lokaalid"]
            surface = None

            distances = []
            surfaces_ids = []
            if use_index:
                for surface_id in surface_idx.intersection(buffered.GetEnvelope()):
                    surface = surfaces.GetFeature(surface_id)
                    if surface.surface_type == SURFACE_TYPE_WATERDEEL:
                        water_geom = surface.geometry()
                        if water_geom.Intersects(buffered):
                            distances.append(water_geom.Distance(surface_geom))
                            surfaces_ids.append(surface["identificatie_lokaalid"])
            else:
                surfaces.SetSpatialFilter(buffered)
                for surface in surfaces:
                    if surface.surface_type == SURFACE_TYPE_WATERDEEL:
                        water_geom = surface.geometry()
                        if water_geom.Intersects(buffered):
                            distances.append(water_geom.Distance(surface_geom))
                            surfaces_ids.append(surface["identificatie_lokaalid"])
                    surface = None

            if len(distances) == 0:
                continue
            else:
                min_dist = min(distances)
                surface_id = surfaces_ids[distances.index(min_dist)]
                out_layer.add_feature(
                    surface_geom, {"surface_lokaalid": surface_id, "distance": min_dist}
                )
            # add to dict
            if surface_id_or not in lokaalid_distances:
                lokaalid_distances[surface_id_or] = {"water_distance": min_dist}
            else:
                lokaalid_distances[surface_id_or]["water_distance"] = min_dist

        out_layer.layer = None

        surfaces.SetSpatialFilter(None)
        surfaces.ResetReading()
        for surface in surfaces:
            lokaalid = surface.identificatie_lokaalid
            if lokaalid in lokaalid_distances.keys():
                data = lokaalid_distances[surface.identificatie_lokaalid]
                for dist_type in DISTANCE_TYPE_NAAM.values():
                    dist_type = "distance_" + dist_type
                    if dist_type in data:
                        surface[dist_type] = data[dist_type]

                if "water_distance" in data:
                    surface["distance_oppervlaktewater"] = data["water_distance"]

                surfaces.SetFeature(surface)
        surfaces = None

    def calculate_runoff_targets(self):
        """
        Fill the 'target type' columns of the result table
        Import BGT Surfaces and Pipes to _database first
        Calculate distances first
        """
        bgt_surfaces = self._database.bgt_surfaces
        result_table = self._database.result_table
        feature_defn = result_table.GetLayerDefn()

        for surface in bgt_surfaces:
            feature = ogr.Feature(feature_defn)
            surface_geometry = surface.GetGeometryRef()
            fixed_geometry = ogr.ForceToPolygon(surface_geometry)
            feature.SetGeometry(fixed_geometry)

            afwatering = self.decision_tree(surface, self.parameters)
            # feature.SetField(RESULT_TABLE_FIELD_ID, val) --> is autoincrement field
            feature.SetField(
                RESULT_TABLE_FIELD_LAATSTE_WIJZIGING,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            feature.SetField(
                RESULT_TABLE_FIELD_BGT_IDENTIFICATIE, surface.identificatie_lokaalid
            )

            feature.SetField(RESULT_TABLE_FIELD_TYPE_VERHARDING, surface.surface_type)
            # feature.SetField(RESULT_TABLE_FIELD_GRAAD_VERHARDING, val) # not yet implemented
            # feature.SetField(RESULT_TABLE_FIELD_HELLINGSTYPE, val) # not yet implemented
            # feature.SetField(RESULT_TABLE_FIELD_HELLINGSPERCENTAGE, val) # not yet implemented
            # feature.SetField(RESULT_TABLE_FIELD_BERGING_DAK, val) # not yet implemented
            # feature.SetField(RESULT_TABLE_FIELD_PUTCODE, val) # not yet implemented
            # feature.SetField(RESULT_TABLE_FIELD_LEIDINGCODE, val) # not yet implemented
            feature.SetField(
                TARGET_TYPE_GEMENGD_RIOOL, afwatering[TARGET_TYPE_GEMENGD_RIOOL]
            )
            feature.SetField(
                TARGET_TYPE_HEMELWATERRIOOL, afwatering[TARGET_TYPE_HEMELWATERRIOOL]
            )
            feature.SetField(
                TARGET_TYPE_VGS_HEMELWATERRIOOL,
                afwatering[TARGET_TYPE_VGS_HEMELWATERRIOOL],
            )
            feature.SetField(
                TARGET_TYPE_INFILTRATIEVOORZIENING,
                afwatering[TARGET_TYPE_INFILTRATIEVOORZIENING],
            )
            feature.SetField(
                TARGET_TYPE_NIET_AANGESLOTEN, afwatering[TARGET_TYPE_NIET_AANGESLOTEN]
            )
            result_table.CreateFeature(feature)
            feature = None


class Database:
    def __init__(self, epsg=28992):
        """
        Constructor
        :param epsg: srid / EPSG code
        """
        self.epsg = epsg
        self.srs = osr.SpatialReference()
        self.srs.ImportFromEPSG(epsg)
        self.mem_database = GPKG_DRIVER.CreateDataSource("/vsimem/_database.gpkg")
        self.register_epsg()
        self.empty_result_table()
        self._sql_dir = SQL_DIR

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
    def buildings(self):
        """Get reference to Pipes layer
        :rtype ogr.Layer
        """
        return self.mem_database.GetLayerByName(BUILDINGS_TABLE_NAME)

    def register_epsg(self):
        """
        Register self.srs in self.mem_database
        Only registers srs if no row of that id exists in gpkg_spatial_ref_sys
        """
        if self.srs.IsProjected():
            cstype = "PROJCS"
        elif self.srs.IsGeographic():
            cstype = "GEOGCS"
        else:
            raise ValueError("Invalid SRS")

        sql = """SELECT * FROM gpkg_spatial_ref_sys WHERE srs_id = {}""".format(
            self.srs.GetAuthorityCode(cstype)
        )
        result_lyr = self.mem_database.ExecuteSQL(sql)
        result_row_count = result_lyr.GetFeatureCount()
        self.mem_database.ReleaseResultSet(result_lyr)
        if result_row_count == 0:
            sql = """
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
                description=self.srs.GetAttrValue(cstype),
            )
            self.mem_database.ExecuteSQL(sql)

    def empty_result_table(self):
        """Create or replace the result table"""
        lyr = self.mem_database.CreateLayer(
            RESULT_TABLE_NAME,
            self.srs,
            geom_type=schema.GEOMETRY_TYPE,
            options=["FID={}".format(schema.PRIMARY_KEY)],
        )  # spatial index is added by default

        for fieldname, datatype in schema.FIELDS.items():
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

    def import_buildings(self, file_path):
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
        bag_ds = ogr.Open(file_path)
        # TODO more thorough checks of validity of input geopackage
        try:
            self.mem_database.CopyLayer(
                bag_ds[0], BUILDINGS_TABLE_NAME
            )
        except Exception:
            # TODO more specific exception
            raise FileInputError(
                "Ongeldige input: {} is geen geldige GWSW GeoPackage".format(
                    gwsw_gpkg_abspath
                )
            )

    def import_surfaces_raw(self, file_path):
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
            for stype in ALL_USED_SURFACE_TYPES:
                surface_source_fn = os.path.join(
                    "/vsizip/" + file_path, "bgt_{stype}.gml".format(stype=stype)
                )
                surface_source = ogr.Open(surface_source_fn)
                src_layer = surface_source.GetLayerByName("{stype}".format(stype=stype))
                self.mem_database.CopyLayer(src_layer=src_layer, new_name=stype)
        except Exception:
            # TODO more specific exception
            raise FileInputError("Ongeldige input: BGT zip file")

    def clean_surfaces(self):
        """
        Update the surfaces layer to include polygons only.
        Linestring features are removed.
        Multipolygons, multisurfaces, curved polygons are forced to polygon.
        """
        for stype in ALL_USED_SURFACE_TYPES:
            lyr = self.mem_database.GetLayerByName(stype)
            lyr.StartTransaction()
            for f in lyr:
                geom = f.GetGeometryRef()
                geom_type = geom.GetGeometryType()
                if geom_type == ogr.wkbPolygon:
                    pass
                elif geom_type == ogr.wkbCurvePolygon:
                    # print('Fixing Curve Polygon feature {}'.format(f.GetFID()))
                    geom_linear = geom.GetLinearGeometry()
                    f.SetGeometry(geom_linear)
                    lyr.SetFeature(f)
                elif geom_type in [ogr.wkbMultiSurface, ogr.wkbMultiPolygon]:
                    # print('Fixing MultiSurface or MultiPolygon feature {}'.format(f.GetFID()))
                    geom_fixed = ogr.ForceToPolygon(geom)
                    f.SetGeometry(geom_fixed)
                    lyr.SetFeature(f)
                elif geom_type in (ogr.wkbLineString, ogr.wkbCompoundCurve):
                    # print('Deleting feature {} because it is a Linestring'.format(f.GetFID()))
                    lyr.DeleteFeature(f.GetFID())
                else:
                    # print('Fixing feature {} failed!'.format(f.GetFID()))
                    raise Exception(
                        "No procedure defined to clean up geometry type {}".format(
                            str(geom_type)
                        )
                    )

            lyr.CommitTransaction()
            lyr = None

    def register_surfaces(self):
        """Register tables in self.mem_database's geopackage admin tables"""
        for stype in ALL_USED_SURFACE_TYPES:
            lyr = self.mem_database.GetLayerByName(stype)
            x0, x1, y0, y1 = lyr.GetExtent()
            sql = """DELETE FROM gpkg_contents WHERE table_name = '{}';""".format(stype)
            self.mem_database.ExecuteSQL(sql)
            sql = """
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
                table_name=stype,
                data_type="features",
                identifier=stype,
                description=stype,
                min_x=x0,
                max_x=x1,
                min_y=y0,
                max_y=y1,
                srs_id=self.epsg,
            )
            self.mem_database.ExecuteSQL(sql)
            sql = """DELETE FROM gpkg_geometry_columns WHERE table_name = '{}';""".format(
                stype
            )
            self.mem_database.ExecuteSQL(sql)
            sql = """
                    INSERT INTO gpkg_geometry_columns (table_name, column_name, geometry_type_name, srs_id, z, m)
                    VALUES ('{table_name}','{column_name}','{geometry_type_name}',{srs_id},{z},{m});
                    """.format(
                table_name=stype,
                column_name="geom",
                geometry_type_name="POLYGON",
                srs_id=28992,
                z=0,
                m=0,
            )
            self.mem_database.ExecuteSQL(sql)

    def classify_surfaces(self, parameters):
        """Determine NWRW surface type of all imported surfaces"""
        layer = self.bgt_surfaces
        if layer is None:
            raise DatabaseOperationError
        # add fields if not exists
        for field_name in [
            RESULT_TABLE_FIELD_TYPE_VERHARDING,
            RESULT_TABLE_FIELD_GRAAD_VERHARDING,
        ]:
            if layer.FindFieldIndex(field_name, 1) == -1:
                field_defn = ogr.FieldDefn(field_name, ogr.OFTString)
                field_defn.SetWidth(60)
                layer.CreateField(field_defn)

        for feature in layer:
            if feature:
                verhardingsgraad = None
                verhardingstype = None 
                if feature.surface_type == SURFACE_TYPE_PAND:
                    verhardingstype = VERHARDINGSTYPE_PAND
                elif feature.surface_type == SURFACE_TYPE_WATERDEEL:
                    verhardingstype = VERHARDINGSTYPE_WATER
                elif feature.surface_type == SURFACE_TYPE_ONDERSTEUNENDWATERDEEL:
                    verhardingstype = VERHARDINGSTYPE_ONVERHARD
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
                    elif feature.bgt_fysiek_voorkomen == "open verharding":
                        verhardingstype = VERHARDINGSTYPE_OPEN_VERHARD
                    elif feature.bgt_fysiek_voorkomen == "half verhard":
                        verhardingstype = VERHARDINGSTYPE_OPEN_VERHARD
                        verhardingsgraad = parameters.verhardingsgraad_half_verhard
                    elif feature.bgt_fysiek_voorkomen == "erf":
                        verhardingstype = VERHARDINGSTYPE_OPEN_VERHARD
                        verhardingsgraad = parameters.verhardingsgraad_erf
                    elif feature.bgt_fysiek_voorkomen == "gesloten verhard":
                        verhardingstype = VERHARDINGSTYPE_GESLOTEN_VERHARD

                feature[RESULT_TABLE_FIELD_TYPE_VERHARDING] = verhardingstype
                if verhardingsgraad is not None:
                    feature[RESULT_TABLE_FIELD_GRAAD_VERHARDING] = verhardingsgraad
                layer.SetFeature(feature)
        layer = None

    def add_build_year_to_surface(self, field_name='bouwjaar', use_index=USE_INDEX):
        surfaces = self.bgt_surfaces
        surfaces.CreateField(ogr.FieldDefn('build_year', ogr.OFTReal))
        if use_index:
            surface_idx = create_index(surfaces)

        for building in self.buildings:
            centroid = building.geometry().Centroid()
            if use_index:
                for surface_id in surface_idx.intersection(centroid.GetEnvelope()):
                    surface = surfaces.GetFeature(surface_id)
                    if surface.surface_type == 'pand':
                        surface['build_year'] = building[field_name]
                        surfaces.SetFeature(surface)
            else:
                surfaces.SetSpatialFilter(centroid)
                for surface in surfaces:
                    if surface.surface_type == 'pand':
                        if surface.geometry().Intersects(centroid):
                            surface['build_year'] = building[field_name]
                            surfaces.SetFeature(surface)
        surfaces = None

    def merge_surfaces(self):
        """ Merge and standardize all imported surfaces to one layer"""
        dest_layer = self.mem_database.CreateLayer(
            SURFACES_TABLE_NAME, self.srs, 3, ["OVERWRITE=YES", "GEOMETRY_NAME=geom"]
        )

        # adding fields to new layer
        add_text_fields = [
            "identificatie_lokaalid",
            "surface_type",
            "bgt_fysiek_voorkomen",
        ]

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
            input_layer = self.mem_database.GetLayerByName("{surface}".format(surface=surface))

            for i in range(0, input_layer.GetFeatureCount()):
                feature = input_layer.GetFeature(i)

                if feature:

                    if feature["eindRegistratie"] is None:
                        if hasattr(feature, "plus-status"):
                            if feature["plus-status"] in ["plan", "historie"]:
                                continue
                        new_feature = ogr.Feature(dest_layer.GetLayerDefn())
                        new_feature.SetField(
                            "identificatie_lokaalid", feature["identificatie.lokaalID"]
                        )
                        new_feature.SetField("surface_type", "{surface}".format(surface=surface))

                        if surface in SURFACE_TYPES_MET_FYSIEK_VOORKOMEN:
                            new_feature["bgt_fysiek_voorkomen"] = feature[
                                "bgt-fysiekVoorkomen"
                            ]

                        target_geometry = ogr.ForceToPolygon(feature.geometry())
                        target_geometry.AssignSpatialReference(self.srs)
                        new_feature.SetGeometry(target_geometry)
                        dest_layer.CreateFeature(new_feature)

                        target_geometry = None
                        new_feature = None
        dest_layer = None

    def _write_to_disk(self, file_path):
        """Copy self.mem_database to file_path"""
        self.out_db = GPKG_DRIVER.CopyDataSource(self.mem_database, file_path)
        self.out_db = None


class Layer(object):
    def __init__(self, layer):
        self.layer = layer
        self.layer_defn = layer.GetLayerDefn()

    def add_feature(self, geometry, attributes):
        """ Append geometry and attributes as new feature. """
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


if __name__ == "__main__":
    pass
