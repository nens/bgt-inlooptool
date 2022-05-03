# System imports
import os
import sys
from pathlib import Path
import configparser

# Third-party imports
from osgeo import osr
from osgeo import gdal
from osgeo import ogr
from datetime import datetime

# Rtree installation
from .rtree_installer import unpack_rtree
unpack_rtree()
sys.path.append(str(Path(__file__).parent.parent))
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


class DatabaseOperationError(Exception):
    """Raised when an invalid _database operation is requested"""
    def __init__(self, msg='Database error', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class FileInputError(Exception):
    """Raised when an attempt is made to import an invalid file"""

    pass


# Drivers
GPKG_DRIVER = ogr.GetDriverByName("GPKG")
MEM_DRIVER = ogr.GetDriverByName("Memory")


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
                 gebruik_bag=GEBRUIK_BAG,
                 gebruik_kolken=GEBRUIK_KOLKEN,
                 bouwjaar_gescheiden_binnenhuisriolering=BOUWJAAR_GESCHEIDEN_BINNENHUISRIOLERING,
                 verhardingsgraad_erf=VERHARDINGSGRAAD_ERF,
                 verhardingsgraad_half_verhard=VERHARDINGSGRAAD_HALF_VERHARD,
                 max_oppervlakte_bgt_vlak=MAX_OPPERVLAKTE_BGT_VLAK):
        self.max_afstand_vlak_afwateringsvoorziening = max_afstand_vlak_afwateringsvoorziening
        self.max_afstand_vlak_oppwater = max_afstand_vlak_oppwater
        self.max_afstand_pand_oppwater = max_afstand_pand_oppwater
        self.max_afstand_vlak_kolk = max_afstand_vlak_kolk
        self.max_afstand_afgekoppeld = max_afstand_afgekoppeld
        self.max_afstand_drievoudig = max_afstand_drievoudig
        self.afkoppelen_hellende_daken = afkoppelen_hellende_daken
        self.gebruik_bag = gebruik_bag
        self.gebruik_kolken = gebruik_kolken
        self.bouwjaar_gescheiden_binnenhuisriolering = bouwjaar_gescheiden_binnenhuisriolering
        self.verhardingsgraad_erf = verhardingsgraad_erf
        self.verhardingsgraad_half_verhard = verhardingsgraad_half_verhard
        self.max_oppervlakte_bgt_vlak = max_oppervlakte_bgt_vlak

    def from_file(self, file):
        
        config = configparser.ConfigParser()
        config.read(file)
        params = config['PARAMETERS']
        
        self.max_afstand_vlak_afwateringsvoorziening=float(params['MAX_AFSTAND_VLAK_AFWATERINGSVOORZIENING'])
        self.max_afstand_vlak_oppwater=float(params['MAX_AFSTAND_VLAK_OPPWATER'])
        self.max_afstand_pand_oppwater=float(params['MAX_AFSTAND_PAND_OPPWATER'])
        self.max_afstand_vlak_kolk=float(params['MAX_AFSTAND_VLAK_KOLK'])
        self.max_afstand_afgekoppeld=float(params['MAX_AFSTAND_AFGEKOPPELD'])
        self.max_afstand_drievoudig=float(params['MAX_AFSTAND_DRIEVOUDIG'])
        self.afkoppelen_hellende_daken=params.getboolean('AFKOPPELEN_HELLENDE_DAKEN')
        self.gebruik_bag=params.getboolean('GEBRUIK_BAG')
        self.gebruik_kolken=params.getboolean('GEBRUIK_KOLKEN')
        self.bouwjaar_gescheiden_binnenhuisriolering=int(params['BOUWJAAR_GESCHEIDEN_BINNENHUISRIOLERING'])
        self.verhardingsgraad_erf=int(params['VERHARDINGSGRAAD_ERF'])
        self.verhardingsgraad_half_verhard=int(params['VERHARDINGSGRAAD_HALF_VERHARD'])
        self.max_oppervlakte_bgt_vlak=float(params['MAX_OPPERVLAKTE_BGT_VLAK'])

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
        self._database.merge_surfaces()
        self._database.classify_surfaces(self.parameters)

    def import_pipes(self, file_path, design=False, pipe_type_field=None, pipe_code_field=None, pipe_map=None, pipe_layer_name=None, relevant_only=True):
        """
        Import pipes to database and classify their type
        :param file_path: path to GWSW Geopackage that contains the pipes
        :param relevant_only: import only the pipes that are used by the InloopTool
        :return: None
        """
        if design:
            self._database.import_pipes(file_path=file_path, layer_name=pipe_layer_name)            
            self._database.classify_pipes_design(pipe_type_field, pipe_code_field, pipe_map)
        else:
            self._database.import_pipes(file_path=file_path, layer_name=pipe_layer_name)
            self._database.classify_pipes_gwsw(delete=relevant_only)            

    def import_kolken(self, file_path):
        """
        Import kolken to database
        :param file_path: path to ogr suitable datasource
        :return: None
        """
        self._database.import_kolken(file_path=file_path)

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
            TARGET_TYPE_VUILWATERRIOOL: 0,
            TARGET_TYPE_INFILTRATIEVOORZIENING: 0,
            TARGET_TYPE_OPEN_WATER: 0,
            TARGET_TYPE_MAAIVELD: 0
        }

        def is_water():
            return surface[RESULT_TABLE_FIELD_TYPE_VERHARDING] == VERHARDINGSTYPE_WATER

        def verhard():
            """Is het oppervlak (mogelijk/deels) verhard?"""
            a = surface.type_verharding
            if surface.surface_type in NON_CONNECTABLE_SURFACE_TYPES:
                return False
            elif surface.type_verharding in {
                VERHARDINGSTYPE_PAND,
                VERHARDINGSTYPE_OPEN_VERHARD,
                VERHARDINGSTYPE_GESLOTEN_VERHARD
            }:
                return True
            else:
                return False

        def bij_hov():
            """Ligt het oppervlak dichtbij een hemelwaterontvangende voorziening?"""
            distances = [surface['distance_' + dt] for dt in DISTANCE_TYPES]
            return min(distances) != PSEUDO_INFINITE

        def is_bouwwerk():
            return surface.surface_type in [SURFACE_TYPE_PAND, SURFACE_TYPE_GEBOUWINSTALLATIE]

        def bij_water():
            return surface['distance_' + OPEN_WATER] < parameters.max_afstand_vlak_oppwater

        def bij_kolk():
            if parameters.gebruik_kolken:
                return surface['distance_' + KOLK] < parameters.max_afstand_vlak_kolk
            else:
                return True

        def bij_gem_plus_hwa():
            """Ligt het oppervlak in de buurt van een straat waar naast gemengd ook rwa is gelegd?"""

            if surface['distance_' + INTERNAL_PIPE_TYPE_GEMENGD_RIOOL] != PSEUDO_INFINITE and (
                    surface['distance_' + INTERNAL_PIPE_TYPE_HEMELWATERRIOOL] != PSEUDO_INFINITE or
                    surface['distance_' + INTERNAL_PIPE_TYPE_INFILTRATIEVOORZIENING] != PSEUDO_INFINITE):
                return abs(
                    surface['distance_' + INTERNAL_PIPE_TYPE_GEMENGD_RIOOL]
                    -
                    min(surface['distance_' + INTERNAL_PIPE_TYPE_HEMELWATERRIOOL],
                        surface['distance_' + INTERNAL_PIPE_TYPE_INFILTRATIEVOORZIENING])
                ) <= parameters.max_afstand_afgekoppeld
            else:
                return False

        def gem_dichtst_bij():
            """Ligt het gemengde riool dichterbij dan HWA/VGS-HWA/Infiltratieriool?"""
            return surface['distance_' + INTERNAL_PIPE_TYPE_GEMENGD_RIOOL] \
                   < \
                   min(
                       surface['distance_' + INTERNAL_PIPE_TYPE_HEMELWATERRIOOL],
                       surface['distance_' + INTERNAL_PIPE_TYPE_INFILTRATIEVOORZIENING]
                   )

        def hwa_dichterbij_dan_hwavgs_en_infiltr():
            """Ligt het HWA riool dichterbij dan het VGS-HWA en het infiltratieriool?"""
            return surface['distance_' + INTERNAL_PIPE_TYPE_HEMELWATERRIOOL] \
                   < \
                   min(
                       surface['distance_' + INTERNAL_PIPE_TYPE_INFILTRATIEVOORZIENING],
                       surface['distance_' + INTERNAL_PIPE_TYPE_VGS_HEMELWATERRIOOL],
                   )

        def bij_drievoudig_stelsel_crit1():
            return False

        def bij_drievoudig_stelsel_crit2():
            return False

        def bij_drievoudig_stelsel_crit3():
            return False

        def hwa_vgs_dichterbij_dan_infiltr():
            return surface['distance_' + INTERNAL_PIPE_TYPE_VGS_HEMELWATERRIOOL] \
                < \
                surface['distance_' + INTERNAL_PIPE_TYPE_INFILTRATIEVOORZIENING]

        def nieuw_pand():
            """Is het bouwjaar van het pand later dan de ondergrens voor gescheiden binnenhuis riolering?"""
            if parameters.gebruik_bag:
                return False
            else:
                if surface.build_year is None:
                    return False
                else:
                    return surface.build_year > parameters.bouwjaar_gescheiden_binnenhuisriolering

        def hellend_dak():
            return True

        for distance_type in DISTANCE_TYPES:
            if surface['distance_' + distance_type] is None:
                surface['distance_' + distance_type] = PSEUDO_INFINITE

        if is_water():
            result[TARGET_TYPE_OPEN_WATER] = 100

        elif not verhard():
            result[TARGET_TYPE_MAAIVELD] = 100

        elif not bij_hov():
            result[TARGET_TYPE_MAAIVELD] = 100

        # PANDEN
        elif is_bouwwerk():
            if bij_water():
                result[TARGET_TYPE_OPEN_WATER] = 100

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
                        if hwa_dichterbij_dan_hwavgs_en_infiltr():
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
                        elif surface['distance_' + INTERNAL_PIPE_TYPE_INFILTRATIEVOORZIENING] != PSEUDO_INFINITE:
                            result[TARGET_TYPE_INFILTRATIEVOORZIENING] = 100
                        else:
                            result[TARGET_TYPE_MAAIVELD] = 100

        # Overige verharde oppervlakken
        elif verhard():
            if bij_water():
                result[TARGET_TYPE_OPEN_WATER] = 100
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
                            elif surface['distance_' + INTERNAL_PIPE_TYPE_INFILTRATIEVOORZIENING] != PSEUDO_INFINITE:
                                result[TARGET_TYPE_INFILTRATIEVOORZIENING] = 100
                            else:
                                result[TARGET_TYPE_MAAIVELD] = 100
                else:
                    result[TARGET_TYPE_MAAIVELD] = 100
        return result

    def calculate_distances(self, parameters):
        """
        For all BGT Surfaces, calculate the distance to:
         * the nearest pipe of each type
         * nearest water surface
         * nearest kolk (sewer gully)

        :param parameters: input parameters
        :return: None
        """
        self.parameters = parameters
        self._database.pipes.ResetReading()
        self._database.pipes.SetSpatialFilter(None)
        self._database.bgt_surfaces.ResetReading()
        self._database.bgt_surfaces.SetSpatialFilter(None)
        
        self.large_surface_pipe_registry = {}
    
        if self.parameters.gebruik_kolken:
            self._database.kolken.ResetReading()
            self._database.kolken.SetSpatialFilter(None)

        surface_water_buffer_dist = max([parameters.max_afstand_pand_oppwater,
                                         parameters.max_afstand_vlak_oppwater])
        
        print(f'surface_water_buffer_dist: {surface_water_buffer_dist}')

        # Distance to pipes
        for surface in self._database.bgt_surfaces:
            if not surface:
                print('surface kapoet')
                continue

            surface_geom = surface.geometry().Clone()
            surface_geom_buffer_afwateringsvoorziening = surface_geom.Buffer(
                parameters.max_afstand_vlak_afwateringsvoorziening
            )
            # Parameters max surface 1000m2?, 'wat is dichtbij', 15m?
            surface_area = surface_geom.Area()

            distances = {}
            pipe_codes = {}
            for pipe_id in self._database.pipes_idx.intersection(
                    surface_geom_buffer_afwateringsvoorziening.GetEnvelope()
            ):
                pipe = self._database.pipes.GetFeature(pipe_id)
                pipe_geom = pipe.geometry().Clone()
                if pipe_geom.Intersects(surface_geom_buffer_afwateringsvoorziening):
                    internal_pipe_type = pipe[INTERNAL_PIPE_TYPE_FIELD]
                    pipe_code = pipe[INTERNAL_PIPE_CODE_FIELD]
                    if internal_pipe_type != INTERNAL_PIPE_TYPE_IGNORE:
                        if internal_pipe_type not in distances.keys():  # Leiding van dit type is nog niet langsgekomen
                            distances[internal_pipe_type] = []
                            pipe_codes[internal_pipe_type] = []
                            distances[internal_pipe_type] += [pipe_geom.Distance(surface_geom)]
                            pipe_codes[internal_pipe_type] += [pipe_code]
                        else:
                            distances[internal_pipe_type] += [pipe_geom.Distance(surface_geom)]
                            pipe_codes[internal_pipe_type] += [pipe_code]
 
            # Distance to water surface
            if surface.surface_type != SURFACE_TYPE_WATERDEEL:
                surface_geom_buffer_surface_water = surface_geom.Buffer(surface_water_buffer_dist)
                min_water_distance = PSEUDO_INFINITE

                for surface_id in self._database.bgt_surfaces_idx.intersection(
                        surface_geom_buffer_surface_water.GetEnvelope()
                ):
                    neighbour_surface = self._database.bgt_surfaces.GetFeature(surface_id)
                    if neighbour_surface.surface_type == SURFACE_TYPE_WATERDEEL:
                        water_geom = neighbour_surface.geometry().Clone()
                        if water_geom.Intersects(surface_geom_buffer_surface_water):
                            dist_to_this_water_surface = water_geom.Distance(surface_geom)
                            if dist_to_this_water_surface < min_water_distance:
                                min_water_distance = dist_to_this_water_surface

                # add to dict
                distances[OPEN_WATER] = min_water_distance

            # Distance to kolk
            if self.parameters.gebruik_kolken:
                if surface.surface_type in KOLK_CONNECTABLE_SURFACE_TYPES:
                    surface_geom_buffer_kolk = surface_geom.Buffer(
                        parameters.max_afstand_vlak_kolk
                    )
                    min_kolk_distance = PSEUDO_INFINITE

                    for kolk_id in self._database.kolken_idx.intersection(
                            surface_geom_buffer_kolk.GetEnvelope()
                    ):
                        kolk = self._database.kolken.GetFeature(kolk_id)
                        kolk_geom = kolk.geometry().Clone()
                        if kolk_geom.Intersects(surface_geom_buffer_kolk):
                            dist_to_this_kolk = kolk_geom.Distance(surface_geom)
                            if dist_to_this_kolk < min_kolk_distance:
                                min_kolk_distance = dist_to_this_kolk

                    # add to dict
                    distances[KOLK] = min_kolk_distance

            # Sort distances and pipe codes
            for distance_type in distances.keys():
                if distance_type not in [KOLK, OPEN_WATER]:
                    distance_list = distances[distance_type]
                    pipe_code_list = pipe_codes[distance_type]
                    distances_sorted, pipe_codes_sorted = map(list, zip(*sorted(zip(distance_list, pipe_code_list))))
                    distances[distance_type] = distances_sorted
                    pipe_codes[distance_type] = pipe_codes_sorted
                    
            # Only register for the large surfaces
            if surface_area > parameters.max_oppervlakte_bgt_vlak:
                self.large_surface_pipe_registry[surface['identificatie_lokaalid']] = [distances, pipe_codes]

            # Write distances to surfaces layer
            for distance_type in DISTANCE_TYPES:

                if distance_type in distances:
                    
                    # Select first distance and pipe code for this type
                    if distance_type in [KOLK, OPEN_WATER]:
                        distance = distances[distance_type]
                    else:                                            
                        distance = distances[distance_type][0]
                        pipe_code = pipe_codes[distance_type][0]
                    
                    if distances[distance_type] == PSEUDO_INFINITE:
                        distances[distance_type] = None

                    surface['distance_' + distance_type] = distance 

                    if distance_type in DISTANCE_PIPE_TYPES:
                        surface['pipe_code_' + distance_type] = pipe_code                        

            self._database.bgt_surfaces.SetFeature(surface)
            surface = None
                
        self._database.bgt_surfaces.ResetReading()
        self._database.bgt_surfaces.SetSpatialFilter(None)


    def calculate_runoff_targets(self, parameters):
        """
        Fill the 'target type' columns of the result table
        Import BGT Surfaces and Pipes to _database first
        Calculate distances first
        """
        bgt_surfaces = self._database.bgt_surfaces
        result_table = self._database.result_table
        feature_defn = result_table.GetLayerDefn()

        for surface in bgt_surfaces:
            
            
            surface_id = surface.identificatie_lokaalid
            feature = ogr.Feature(feature_defn)
            surface_geometry = surface.GetGeometryRef()
            fixed_geometry = ogr.ForceToPolygon(surface_geometry)
            feature.SetGeometry(fixed_geometry)
                 
            feature_area = fixed_geometry.Area()
                                
            # If the surface is larger than the given max area
            # Calculate what system it should go to 
            # Divide into the max possible amount of sub surfaces using the large surface pipe distance dictionary
             
            afwatering = self.decision_tree(surface, self.parameters)
            if feature_area > parameters.max_oppervlakte_bgt_vlak and afwatering[TARGET_TYPE_OPEN_WATER] != 100 and afwatering[TARGET_TYPE_MAAIVELD] != 100:
                                
                for tt in TARGET_TYPES:
                    if afwatering[tt] > 0 and tt in DISTANCE_PIPE_TYPES:
                        # If the afwatering is larger than 0, we find how many pipes this should be divided to
                        # Optional to limit the amount of pipes by selecting within a certain distance
                        distance_list = self.large_surface_pipe_registry[surface_id][0][tt]
                        pipe_code_list = self.large_surface_pipe_registry[surface_id][1][tt]
                        percentage_afwatering_distance_type = afwatering[tt]
                        percentage_split = percentage_afwatering_distance_type / len(distance_list)
                        for i in range(0,len(distance_list)):
                            split_feature = ogr.Feature(feature_defn)
                            split_feature.SetGeometry(fixed_geometry)
                                                    
                            split_feature.SetField(
                                RESULT_TABLE_FIELD_ID,
                                surface.GetFID(),
                            )
                            split_feature.SetField(
                                RESULT_TABLE_FIELD_LAATSTE_WIJZIGING,
                                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            )
                            split_feature.SetField(
                                RESULT_TABLE_FIELD_BGT_IDENTIFICATIE, surface.identificatie_lokaalid
                            )
                
                            split_feature.SetField(RESULT_TABLE_FIELD_TYPE_VERHARDING, surface.type_verharding)
                            split_feature.SetField(RESULT_TABLE_FIELD_GRAAD_VERHARDING, surface.graad_verharding)
                            split_feature.SetField(tt, percentage_split)
                            # Set other target types to 0
                            for tt_other in TARGET_TYPES:
                                if tt_other != tt:
                                    split_feature.SetField(tt_other, 0)
                            
                            split_feature.SetField('pipe_code_'+tt, pipe_code_list[i])
                            
                            result_table.CreateFeature(split_feature)
                            split_feature = None
                            
            else:
                feature.SetField(
                    RESULT_TABLE_FIELD_ID,
                    surface.GetFID(),
                )
                feature.SetField(
                    RESULT_TABLE_FIELD_LAATSTE_WIJZIGING,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )
                feature.SetField(
                    RESULT_TABLE_FIELD_BGT_IDENTIFICATIE, surface.identificatie_lokaalid
                )
    
                feature.SetField(RESULT_TABLE_FIELD_TYPE_VERHARDING, surface.type_verharding)
                feature.SetField(RESULT_TABLE_FIELD_GRAAD_VERHARDING, surface.graad_verharding)
                # feature.SetField(RESULT_TABLE_FIELD_HELLINGSTYPE, val) # not yet implemented
                # feature.SetField(RESULT_TABLE_FIELD_HELLINGSPERCENTAGE, val) # not yet implemented
                # feature.SetField(RESULT_TABLE_FIELD_BERGING_DAK, val) # not yet implemented
                # feature.SetField(RESULT_TABLE_FIELD_PUTCODE, val) # not yet implemented
                #feature.SetField(RESULT_TABLE_FIELD_LEIDINGCODE, surface.) # not yet implemented
                for tt in TARGET_TYPES:
                    feature.SetField(tt, afwatering[tt])
                    
                    if tt in DISTANCE_PIPE_TYPES:
                        feature.SetField('pipe_code_'+tt, surface['pipe_code_'+tt])
                        
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
        self.mem_database = MEM_DRIVER.CreateDataSource('')
        self.create_table(table_name=RESULT_TABLE_NAME, table_schema=RESULT_TABLE_SCHEMA)

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

    def create_table(self, table_name, table_schema):
        """Create or replace the result table
        :param table_schema:
        :param table_name:
        """
        lyr = self.mem_database.CreateLayer(
            table_name,
            self.srs,
            geom_type=table_schema.geometry_type
        )

        for fieldname, datatype in table_schema.fields.items():
            field_defn = ogr.FieldDefn(fieldname, datatype)
            lyr.CreateField(field_defn)

        lyr = None

    def import_pipes(self, layer_name, file_path):
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
                lines_ds.GetLayerByName(layer_name), PIPES_TABLE_NAME
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
            nr_layers_with_features = 0
            for stype in ALL_USED_SURFACE_TYPES:
                surface_source_fn = os.path.join(
                    "/vsizip/" + file_path, "bgt_{stype}.gml".format(stype=stype)
                )
                if stype in MULTIPLE_GEOMETRY_SURFACE_TYPES:
                    surface_source_gfs_fn = os.path.join(GFS_DIR, f'bgt_{stype}.gfs')
                    if not os.path.isfile(surface_source_gfs_fn):
                        raise ValueError(f'GFS file for {stype} not found')
                    surface_source = gdal.OpenEx(surface_source_fn,
                                                 open_options=[f'GFS_TEMPLATE={surface_source_gfs_fn}'])
                else:
                    surface_source = ogr.Open(surface_source_fn)
                if surface_source is None:
                    continue  # TODO Warning
                else:
                    src_layer = surface_source.GetLayerByName("{stype}".format(stype=stype))
                    if src_layer is None:
                        continue  # TODO Warning
                    else:
                        nr_layers_with_features += 1
                        self.mem_database.CopyLayer(src_layer=src_layer, new_name=stype)
                        print(f'raw import of {stype} layer has {self.mem_database.GetLayerByName(stype).GetFeatureCount()} features')
            if nr_layers_with_features == 0:
                raise FileInputError(f"BGT zip file is leeg of bevat alleen lagen zonder features")
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
            raise FileNotFoundError(
                "Bestand niet gevonden: {}".format(kolken_abspath)
            )
        # TODO more thorough checks of validity of input geopackage

        try:
            kolken_ds = ogr.Open(file_path)
            self.mem_database.CopyLayer(
                kolken_ds[0], KOLKEN_TABLE_NAME
            )
        except Exception:
            # TODO more specific exception
            raise FileInputError(
                "Ongeldige input: {}".format(kolken_abspath
                                             )
            )

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


        for pipe_id in self.pipes_idx.intersection(extent_geometry.GetEnvelope()):
            pipe = pipes.GetFeature(pipe_id)
            pipe_geom = pipe.geometry()
            if pipe_geom.Intersects(extent_geometry):
                intersecting_pipes.append(pipe_id)

        for surface_id in self.bgt_surfaces_idx.intersection(extent_geometry.GetEnvelope()):
            surface = bgt_surfaces.GetFeature(surface_id)
            surface_geom = surface.geometry()
            if surface_geom.Intersects(extent_geometry):
                intersecting_surfaces.append(surface_id)


        for pipe in pipes:
            pipe_fid = pipe.GetFID()
            if pipe_fid not in intersecting_pipes:
                pipes.DeleteFeature(pipe_fid)

        for surface in bgt_surfaces:
            surface_fid = surface.GetFID()
            if surface_fid not in intersecting_surfaces:
                bgt_surfaces.DeleteFeature(surface_fid)

        pipes = None
        bgt_surfaces = None

    def clean_surfaces(self):
        """
        Update the surfaces layer to include polygons only.
        Linestring features are removed.
        Multipolygons, multisurfaces, curved polygons are forced to polygon.
        
        """
        for stype in ALL_USED_SURFACE_TYPES:
            lyr = self.mem_database.GetLayerByName(stype)
            if lyr is None:  # this happens if this particular layer in the bgt input has no features
                continue
            lyr.ResetReading()
            delete_fids = []
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
                    geom_fixed = geom_fixed.MakeValid()
                    if geom_fixed.GetGeometryType() == ogr.wkbMultiPolygon:
                        for subgeom in geom_fixed:
                            if subgeom.GetGeometryType() == ogr.wkbPolygon:
                                cf = f.Clone()
                                cf.SetGeometry(subgeom)
                                lyr.SetFeature(cf)
                    else:
                        f.SetGeometry(geom_fixed)
                        lyr.SetFeature(f)
                        
                elif geom_type in (ogr.wkbLineString, ogr.wkbCompoundCurve, ogr.wkbCircularString):
                    # print('Deleting feature {} because it is a Linestring'.format(f.GetFID()))
                    delete_fids.append(f.GetFID())
                else:
                    print('Warning: Fixing feature {fid} in {stype} failed! No procedure defined to clean up geometry '
                          'type {geom_type}. Continuing anyway.'.format(fid=f.GetFID(), stype=stype, geom_type=str(geom_type))
                          )
                    continue
            for fid in delete_fids:
                lyr.DeleteFeature(fid)
            print(f'cleaned import of {stype} layer has {lyr.GetFeatureCount()} features')

            lyr = None
            
    def split_polygons(self, parameters):
        """Split all polygons that exceed a given area into equal parts"""
        pass

    def classify_pipes_gwsw(self, delete=True):
        """Assign pipe type based on GWSW pipe type. Optionally, delete pipes of type INTERNAL_PIPE_TYPE_IGNORE"""
        layer = self.mem_database.GetLayerByName(PIPES_TABLE_NAME)
        if layer is None:
            raise DatabaseOperationError

        layer.CreateField(ogr.FieldDefn(INTERNAL_PIPE_TYPE_FIELD, ogr.OFTString))

        delete_fids = []
        for pipe_feat in layer:
            if pipe_feat:
                gwsw_pipe_type_uri = pipe_feat[GWSW_PIPE_TYPE_FIELD]
                gwsw_pipe_type_clean = gwsw_pipe_type_uri.split('/')[-1]
                try:
                    internal_pipe_type = PIPE_MAP[gwsw_pipe_type_clean]
                except KeyError:
                    internal_pipe_type = INTERNAL_PIPE_TYPE_IGNORE
                if internal_pipe_type == INTERNAL_PIPE_TYPE_IGNORE:
                    delete_fids.append(pipe_feat.GetFID())
                elif internal_pipe_type == INTERNAL_PIPE_TYPE_HEMELWATERRIOOL:
                    gwsw_stelsel_type_uri = pipe_feat[GWSW_STELSEL_TYPE_FIELD]
                    gwsw_stelsel_type_clean = gwsw_pipe_type_uri.split('/')[-1]
                    if gwsw_stelsel_type_clean == GWSW_STELSEL_TYPE_VERBETERDHEMELWATERSTELSEL:
                        internal_pipe_type = INTERNAL_PIPE_TYPE_VGS_HEMELWATERRIOOL
                pipe_feat[INTERNAL_PIPE_TYPE_FIELD] = internal_pipe_type
                layer.SetFeature(pipe_feat)

        if delete:
            for fid in delete_fids:
                layer.DeleteFeature(fid)

        layer = None
        
    def classify_pipes_design(self, pipe_type_field, pipe_code_field, pipe_map, delete=True):

        """Classify pipes from a design input with a custom field mapping"""
            
        # Rename the code field to INTERNAL_PIPE_CODE_FIELD
        # Map fields for: gemengd_riool, hemelwaterriool, vgs_hemelwaterriool, infiltratievoorziening
        # pipe_map= {'gemengd': 'gemengd_riool', 'hemelwater':'hemelwaterriool', 'vgs':vgs_hemelwaterriool}

        layer = self.mem_database.GetLayerByName(PIPES_TABLE_NAME)
        if layer is None:
            raise DatabaseOperationError('Failed to open pipes layer')
            
        # Rename the code field to the internal used code field
        layer_dfn = layer.GetLayerDefn()
        field_idx = layer.FindFieldIndex(pipe_code_field,1)
                
        if field_idx != -1:
            field_dfn = layer_dfn.GetFieldDefn(field_idx)
            field_dfn.SetName(INTERNAL_PIPE_CODE_FIELD)
            field_dfn = None
        else:
            raise DatabaseOperationError('Pipe code field not in layer')

        layer.CreateField(ogr.FieldDefn(INTERNAL_PIPE_TYPE_FIELD, ogr.OFTString))

        delete_fids = []
        for pipe_feat in layer:
            if pipe_feat:
                pipe_type = pipe_feat.GetField(pipe_type_field)
                try:
                    internal_pipe_type = pipe_map[pipe_type]
                except KeyError:
                    internal_pipe_type = INTERNAL_PIPE_TYPE_IGNORE
                if internal_pipe_type == INTERNAL_PIPE_TYPE_IGNORE:
                    delete_fids.append(pipe_feat.GetFID())
    
                pipe_feat[INTERNAL_PIPE_TYPE_FIELD] = internal_pipe_type
                layer.SetFeature(pipe_feat)

        if delete:
            for fid in delete_fids:
                layer.DeleteFeature(fid)

        layer = None


    def classify_surfaces(self, parameters):
        """Determine NWRW surface type of all imported surfaces"""
        layer = self.mem_database.GetLayerByName(SURFACES_TABLE_NAME)
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
                        verhardingsgraad = parameters.verhardingsgraad_half_verhard
                    elif feature.bgt_fysiek_voorkomen == "erf":
                        if parameters.verhardingsgraad_erf > 0:
                            verhardingstype = VERHARDINGSTYPE_OPEN_VERHARD
                        else:
                            verhardingstype = VERHARDINGSTYPE_ONVERHARD
                        verhardingsgraad = parameters.verhardingsgraad_erf
                    elif feature.bgt_fysiek_voorkomen == "gesloten verharding":
                        verhardingstype = VERHARDINGSTYPE_GESLOTEN_VERHARD
                        verhardingsgraad = 100
                feature[RESULT_TABLE_FIELD_TYPE_VERHARDING] = verhardingstype
                if verhardingsgraad is not None:
                    feature[RESULT_TABLE_FIELD_GRAAD_VERHARDING] = verhardingsgraad
                layer.SetFeature(feature)
        layer = None

    def merge_surfaces(self):
        """ Merge and standardize all imported surfaces to one layer"""
        self.create_table(table_name=SURFACES_TABLE_NAME, table_schema=SURFACES_TABLE_SCHEMA)
        dest_layer = self.mem_database.GetLayerByName(SURFACES_TABLE_NAME)
        id_counter = 1
        previous_fcount = 0
        for stype in ALL_USED_SURFACE_TYPES:
            input_layer = self.mem_database.GetLayerByName(stype)
            if input_layer is None:  # this happens if this particular layer in the bgt input has no features
                continue
            for feature in input_layer:
                if hasattr(feature, "eindRegistratie"):
                    if feature["eindRegistratie"] is not None:
                        continue
                if hasattr(feature, "plus-status"):
                    if feature["plus-status"] in ["plan", "historie"]:
                        continue
                new_feature = ogr.Feature(dest_layer.GetLayerDefn())
                new_feature.SetField('id', id_counter)
                id_counter += 1
                new_feature.SetField(
                    "identificatie_lokaalid", feature["identificatie.lokaalID"]
                )
                new_feature.SetField("surface_type", stype)

                if stype in SURFACE_TYPES_MET_FYSIEK_VOORKOMEN:
                    new_feature["bgt_fysiek_voorkomen"] = feature[
                        "bgt-fysiekVoorkomen"
                    ]

                if stype == SURFACE_TYPE_PAND:
                    new_feature['identificatiebagpnd'] = feature['identificatieBAGPND']

                target_geometry = ogr.ForceToPolygon(feature.geometry())
                target_geometry.AssignSpatialReference(self.srs)
                new_feature.SetGeometry(target_geometry)
                dest_layer.CreateFeature(new_feature)
                target_geometry = None
                new_feature = None
            print(f'added {dest_layer.GetFeatureCount()-previous_fcount} features from {stype} layer')
            previous_fcount = dest_layer.GetFeatureCount()
        dest_layer = None

    def add_build_year_to_surface(self, file_path, field_name='bouwjaar'):

        print('Started add_build_year_to_surface...')

        ds = ogr.Open(file_path)
        buildings = ds[0]

        surfaces = self.bgt_surfaces
        surfaces.ResetReading()
        surfaces.CreateField(ogr.FieldDefn('build_year', ogr.OFTReal))

        # create dict from buildings
        building_dict = {}
        for building in buildings:
            building_dict[building['identificatie'][1:]] = building[field_name]
            building = None

        for surface in surfaces:
            if surface['surface_type'] == SURFACE_TYPE_PAND:
                if surface['identificatiebagpnd'] in building_dict.keys():
                    surface['build_year'] = building_dict[surface['identificatiebagpnd']]
                    surfaces.SetFeature(surface)
            surface = None

        buildings = None
        surfaces = None
        print('... done')
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
