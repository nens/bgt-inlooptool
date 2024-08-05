# System imports
import os
import sys

# Third-party imports
from osgeo import osr
from osgeo import gdal
from osgeo import ogr
from datetime import datetime

try: # Rtree should be installed by the plugin for QGIS
    import rtree  
except ImportError: # For ArcGIS Pro the following is needed
    import sys
    from pathlib import Path
    
    try:
        from .rtree_installer import unpack_rtree
        if not str(Path(__file__).parent) in sys.path:  # bgt_inlooptool\\core
            rtree_path = unpack_rtree()
            sys.path.append(str(rtree_path))
    except ImportError:
        print("The 'rtree' package installation failed.")
    
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

    pass


class FileInputError(Exception):
    """Raised when an attempt is made to import an invalid file"""

    pass


# Drivers
GPKG_DRIVER = ogr.GetDriverByName("GPKG")
MEM_DRIVER = ogr.GetDriverByName("Memory")


class InputParameters:
    """Parameters that determine the behaviour of the tool"""

    def __init__(
        self,
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
    ):
        self.max_afstand_vlak_afwateringsvoorziening = (
            max_afstand_vlak_afwateringsvoorziening
        )
        self.max_afstand_vlak_oppwater = max_afstand_vlak_oppwater
        self.max_afstand_pand_oppwater = max_afstand_pand_oppwater
        self.max_afstand_vlak_kolk = max_afstand_vlak_kolk
        self.max_afstand_afgekoppeld = max_afstand_afgekoppeld
        self.max_afstand_drievoudig = max_afstand_drievoudig
        self.afkoppelen_hellende_daken = afkoppelen_hellende_daken
        self.gebruik_bag = gebruik_bag
        self.gebruik_kolken = gebruik_kolken
        self.bouwjaar_gescheiden_binnenhuisriolering = (
            bouwjaar_gescheiden_binnenhuisriolering
        )
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
        
    def set_settings_start(self,bgt_file,pipe_file,building_file, kolken_file):
        settings_table = self._database.settings_table
        feature_defn = settings_table.GetLayerDefn()
        feature = ogr.Feature(feature_defn)
        
        max_fid = -1
        for feature in settings_table:
            fid = feature.GetFID()
            if fid > max_fid:
                max_fid = fid
        
        if feature is None: 
            new_fid = 1
        else:
            new_fid = max_fid + 1
        """
        feature.SetField(
            "fid",
            new_fid,
        )#to do: kan het zonder fid?
        """
        feature.SetField(
            SETTINGS_TABLE_FIELD_ID,
            new_fid,
        )
        feature.SetField(
            SETTINGS_TABLE_FIELD_TIJD_START,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        feature.SetField(
            SETTINGS_TABLE_FIELD_DOWNLOAD_BGT, 0
        )
        feature.SetField(
            SETTINGS_TABLE_FIELD_DOWNLOAD_GWSW, 0
        )
        feature.SetField(
            SETTINGS_TABLE_FIELD_DOWNLOAD_BAG, 0
        )
        feature.SetField(
            SETTINGS_TABLE_FIELD_PAD_BGT, bgt_file
        )
        feature.SetField(
            SETTINGS_TABLE_FIELD_PAD_GWSW, pipe_file
        )
        feature.SetField(
            SETTINGS_TABLE_FIELD_PAD_BAG, building_file
        )
        feature.SetField(
            SETTINGS_TABLE_FIELD_PAD_KOLKEN, kolken_file
        )
        feature.SetField(
            SETTINGS_TABLE_FIELD_AFSTAND_AFWATERINGSVOORZIENING, self.parameters.max_afstand_vlak_afwateringsvoorziening
        )
        feature.SetField(
            SETTINGS_TABLE_FIELD_AFSTAND_VERHARD_OPP_WATER, self.parameters.max_afstand_vlak_oppwater
        )
        feature.SetField(
            SETTINGS_TABLE_FIELD_AFSTAND_PAND_OPP_WATER, self.parameters.max_afstand_pand_oppwater
        )
        feature.SetField(
            SETTINGS_TABLE_FIELD_AFSTAND_VERHARD_KOLK, self.parameters.max_afstand_vlak_kolk
        )
        feature.SetField(
            SETTINGS_TABLE_FIELD_AFSTAND_AFKOPPELD, self.parameters.max_afstand_afgekoppeld
        )
        feature.SetField(
            SETTINGS_TABLE_FIELD_AFSTAND_DRIEVOUDIG, self.parameters.max_afstand_drievoudig
        )
        feature.SetField(
            SETTINGS_TABLE_FIELD_VERHARDINGSGRAAD_ERF, self.parameters.verhardingsgraad_erf
        )
        feature.SetField(
            SETTINGS_TABLE_FIELD_VERHARDINGSGRAAD_HALF_VERHARD, self.parameters.verhardingsgraad_half_verhard
        )
        feature.SetField(
            SETTINGS_TABLE_FIELD_AFKOPPELEN_HELLEND, self.parameters.afkoppelen_hellende_daken
        )
        feature.SetField(
            SETTINGS_TABLE_FIELD_BOUWJAAR_GESCHEIDEN_BINNENHUIS, self.parameters.bouwjaar_gescheiden_binnenhuisriolering
        )
        
        settings_table.CreateFeature(feature)
        feature = None
        settings_table = None
        
    def set_settings_end(self):
        # Find the feature with the highest FID
        max_fid = -1
        feature_to_update = None
        
        settings_table = self._database.settings_table
        
        for feature in settings_table:
            fid = feature.GetFID()
            if fid > max_fid:
                max_fid = fid
                feature_to_update = feature
        
        if feature_to_update is not None:
            # Set the new value for the specified field
            feature_to_update.SetField(
                        SETTINGS_TABLE_FIELD_TIJD_EIND,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    )

            # Update the feature in the layer
            settings_table.SetFeature(feature_to_update)
            
            print("Test_output")
            # Print all field names and their values
            feature_defn = feature_to_update.GetDefnRef()
            print("Feature ID:", feature_to_update.GetFID())
            for i in range(feature_defn.GetFieldCount()):
                field_defn = feature_defn.GetFieldDefn(i)
                field_name = field_defn.GetName()
                field_value = feature_to_update.GetField(i)
                print(f"{field_name}: {field_value}")
            
            # Clean up
            feature_to_update = None
            settings_table = None
            print(f"Feature with FID {max_fid} updated successfully.")
        else:
            print("No features found in the layer.")
        
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

    def import_pipes(self, file_path, relevant_only=True):
        """
        Import pipes to database and classify their type
        :param file_path: path to GWSW Geopackage that contains the pipes
        :param relevant_only: import only the pipes that are used by the InloopTool
        :return: None
        """
        self._database.import_pipes(file_path=file_path)
        self._database.classify_pipes(delete=relevant_only)

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
            TARGET_TYPE_MAAIVELD: 0,
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
                VERHARDINGSTYPE_GESLOTEN_VERHARD,
            }:
                return True
            else:
                return False

        def bij_hov():
            """Ligt het oppervlak dichtbij een hemelwaterontvangende voorziening?"""
            distances = [surface["distance_" + dt] for dt in DISTANCE_TYPES]
            return min(distances) != PSEUDO_INFINITE

        def is_bouwwerk():
            return surface.surface_type in [
                SURFACE_TYPE_PAND,
                SURFACE_TYPE_GEBOUWINSTALLATIE,
            ]

        def bij_water():
            return (
                surface["distance_" + OPEN_WATER] < parameters.max_afstand_vlak_oppwater
            )

        def bij_kolk():
            if parameters.gebruik_kolken:
                return surface["distance_" + KOLK] < parameters.max_afstand_vlak_kolk
            else:
                return True

        def bij_gem_plus_hwa():
            """Ligt het oppervlak in de buurt van een straat waar naast gemengd ook rwa is gelegd?"""

            if surface[
                "distance_" + INTERNAL_PIPE_TYPE_GEMENGD_RIOOL
            ] != PSEUDO_INFINITE and (
                surface["distance_" + INTERNAL_PIPE_TYPE_HEMELWATERRIOOL]
                != PSEUDO_INFINITE
                or surface["distance_" + INTERNAL_PIPE_TYPE_INFILTRATIEVOORZIENING]
                != PSEUDO_INFINITE
            ):
                return (
                    abs(
                        surface["distance_" + INTERNAL_PIPE_TYPE_GEMENGD_RIOOL]
                        - min(
                            surface["distance_" + INTERNAL_PIPE_TYPE_HEMELWATERRIOOL],
                            surface[
                                "distance_" + INTERNAL_PIPE_TYPE_INFILTRATIEVOORZIENING
                            ],
                        )
                    )
                    <= parameters.max_afstand_afgekoppeld
                )
            else:
                return False

        def gem_dichtst_bij():
            """Ligt het gemengde riool dichterbij dan HWA/VGS-HWA/Infiltratieriool?"""
            return surface["distance_" + INTERNAL_PIPE_TYPE_GEMENGD_RIOOL] < min(
                surface["distance_" + INTERNAL_PIPE_TYPE_HEMELWATERRIOOL],
                surface["distance_" + INTERNAL_PIPE_TYPE_INFILTRATIEVOORZIENING],
            )

        def hwa_dichterbij_dan_hwavgs_en_infiltr():
            """Ligt het HWA riool dichterbij dan het VGS-HWA en het infiltratieriool?"""
            return surface["distance_" + INTERNAL_PIPE_TYPE_HEMELWATERRIOOL] < min(
                surface["distance_" + INTERNAL_PIPE_TYPE_INFILTRATIEVOORZIENING],
                surface["distance_" + INTERNAL_PIPE_TYPE_VGS_HEMELWATERRIOOL],
            )

        def bij_drievoudig_stelsel_crit1():
            return False

        def bij_drievoudig_stelsel_crit2():
            return False

        def bij_drievoudig_stelsel_crit3():
            return False

        def hwa_vgs_dichterbij_dan_infiltr():
            return (
                surface["distance_" + INTERNAL_PIPE_TYPE_VGS_HEMELWATERRIOOL]
                < surface["distance_" + INTERNAL_PIPE_TYPE_INFILTRATIEVOORZIENING]
            )

        def nieuw_pand():
            """Is het bouwjaar van het pand later dan de ondergrens voor gescheiden binnenhuis riolering?"""
            if parameters.gebruik_bag:
                if surface.build_year is None:
                    return False
                else:
                    return (
                        surface.build_year
                        > parameters.bouwjaar_gescheiden_binnenhuisriolering
                    )
            else:
                return False

        def hellend_dak():
            return True

        for distance_type in DISTANCE_TYPES:
            if surface["distance_" + distance_type] is None:
                surface["distance_" + distance_type] = PSEUDO_INFINITE

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
                        if hwa_dichterbij_dan_hwavgs_en_infiltr():
                            result[TARGET_TYPE_HEMELWATERRIOOL] = 100
                        else:
                            if hwa_vgs_dichterbij_dan_infiltr():
                                result[TARGET_TYPE_VGS_HEMELWATERRIOOL] = 100
                            else:
                                result[TARGET_TYPE_INFILTRATIEVOORZIENING] = 100
                    else:
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
                        elif (
                            surface[
                                "distance_" + INTERNAL_PIPE_TYPE_INFILTRATIEVOORZIENING
                            ]
                            != PSEUDO_INFINITE
                        ):
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
                            elif (
                                surface[
                                    "distance_"
                                    + INTERNAL_PIPE_TYPE_INFILTRATIEVOORZIENING
                                ]
                                != PSEUDO_INFINITE
                            ):
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

        if self.parameters.gebruik_kolken:
            self._database.kolken.ResetReading()
            self._database.kolken.SetSpatialFilter(None)

        surface_water_buffer_dist = max(
            [parameters.max_afstand_pand_oppwater, parameters.max_afstand_vlak_oppwater]
        )
        print(f"surface_water_buffer_dist: {surface_water_buffer_dist}")

        # Distance to pipes
        for surface in self._database.bgt_surfaces:
            if not surface:
                print("surface kapoet")
                continue

            surface_geom = surface.geometry().Clone()
            surface_geom_buffer_afwateringsvoorziening = surface_geom.Buffer(
                parameters.max_afstand_vlak_afwateringsvoorziening
            )

            distances = {}
            for pipe_id in self._database.pipes_idx.intersection(
                surface_geom_buffer_afwateringsvoorziening.GetEnvelope()
            ):
                pipe = self._database.pipes.GetFeature(pipe_id)
                pipe_geom = pipe.geometry().Clone()
                if pipe_geom.Intersects(surface_geom_buffer_afwateringsvoorziening):
                    internal_pipe_type = pipe[INTERNAL_PIPE_TYPE_FIELD]
                    if internal_pipe_type != INTERNAL_PIPE_TYPE_IGNORE:
                        if (
                            internal_pipe_type not in distances.keys()
                        ):  # Leiding van dit type is nog niet langsgekomen
                            distances[internal_pipe_type] = pipe_geom.Distance(
                                surface_geom
                            )
                        else:
                            if distances[internal_pipe_type] > pipe_geom.Distance(
                                surface_geom
                            ):
                                distances[internal_pipe_type] = pipe_geom.Distance(
                                    surface_geom
                                )

            # Distance to water surface
            if surface.surface_type != SURFACE_TYPE_WATERDEEL:
                surface_geom_buffer_surface_water = surface_geom.Buffer(
                    surface_water_buffer_dist
                )
                min_water_distance = PSEUDO_INFINITE

                for surface_id in self._database.bgt_surfaces_idx.intersection(
                    surface_geom_buffer_surface_water.GetEnvelope()
                ):
                    neighbour_surface = self._database.bgt_surfaces.GetFeature(
                        surface_id
                    )
                    if neighbour_surface.surface_type == SURFACE_TYPE_WATERDEEL:
                        water_geom = neighbour_surface.geometry().Clone()
                        if water_geom.Intersects(surface_geom_buffer_surface_water):
                            dist_to_this_water_surface = water_geom.Distance(
                                surface_geom
                            )
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

            # Write distances to surfaces layer
            for distance_type in DISTANCE_TYPES:

                if distance_type in distances:
                    if distances[distance_type] == PSEUDO_INFINITE:
                        distances[distance_type] = None
                    surface["distance_" + distance_type] = distances[distance_type]

            self._database.bgt_surfaces.SetFeature(surface)
            surface = None

        self._database.bgt_surfaces.ResetReading()
        self._database.bgt_surfaces.SetSpatialFilter(None)

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

            feature.SetField(
                RESULT_TABLE_FIELD_TYPE_VERHARDING, surface.type_verharding
            )
            feature.SetField(
                RESULT_TABLE_FIELD_GRAAD_VERHARDING, surface.graad_verharding
            )
            feature.SetField(
                "surface_type", surface.surface_type
                )
            feature.SetField(
                "bgt_fysiek_voorkomen", surface.bgt_fysiek_voorkomen #Deze nog aanpassen
                )
            feature.SetField(
                "build_year", surface.build_year
                )
            feature.SetField(
                RESULT_TABLE_FIELD_WIJZIGING, 0
            )
            # feature.SetField(RESULT_TABLE_FIELD_HELLINGSTYPE, val) # not yet implemented
            # feature.SetField(RESULT_TABLE_FIELD_HELLINGSPERCENTAGE, val) # not yet implemented
            # feature.SetField(RESULT_TABLE_FIELD_BERGING_DAK, val) # not yet implemented
            # feature.SetField(RESULT_TABLE_FIELD_PUTCODE, val) # not yet implemented
            # feature.SetField(RESULT_TABLE_FIELD_LEIDINGCODE, val) # not yet implemented
            for tt in TARGET_TYPES:
                feature.SetField(tt, afwatering[tt])
            result_table.CreateFeature(feature)
            feature = None

    def calculate_statistics(self,stats_path):
        dest_layer = self._database.statistics_table
        stats_abspath = os.path.abspath(stats_path)
        it_layer = self._database.result_table
        
        if not os.path.isfile(stats_abspath):
            raise FileNotFoundError(
                "Shapefile met gebieden voor statistieken niet gevonden: {}".format(stats_abspath)
            )
        stats_ds = ogr.Open(stats_path)
        stats_layer = stats_ds.GetLayer()
        
        gebied_id = 0
        #Write geometries of shapefile features to db and calculate the statistics
        for feature in stats_layer:
            gebied_id += 1
            # Create a new feature with the same geometry
            geom = feature.GetGeometryRef()
            new_feature = ogr.Feature(dest_layer.GetLayerDefn())
            new_feature.SetGeometry(geom.Clone())
            
            #Set gebied_ID
            new_feature.SetField(
                STATISTICS_TABLE_FIELD_ID,gebied_id
            )
            
            # Calculate statistics
            new_feature.SetField(
                STATISTICS_TABLE_FIELD_OPP_TOTAAL,self.calculate_intersection_area(it_layer, new_feature, "total")
            )
            new_feature.SetField(
                STATISTICS_TABLE_FIELD_OPP_GEMENGD,self.calculate_intersection_area(it_layer, new_feature, "gemengd")
            )
            new_feature.SetField(
                STATISTICS_TABLE_FIELD_OPP_HWA,self.calculate_intersection_area(it_layer, new_feature, "hwa")
            )
            new_feature.SetField(
                STATISTICS_TABLE_FIELD_OPP_VGS,self.calculate_intersection_area(it_layer, new_feature, "vgs")
            )
            new_feature.SetField(
                STATISTICS_TABLE_FIELD_OPP_DWA,self.calculate_intersection_area(it_layer, new_feature, "dwa")
            )
            new_feature.SetField(
                STATISTICS_TABLE_FIELD_OPP_INFIL,self.calculate_intersection_area(it_layer, new_feature, "infil")
            )
            new_feature.SetField(
                STATISTICS_TABLE_FIELD_OPP_OPEN_WATER,self.calculate_intersection_area(it_layer, new_feature,"open_water")
            )
            new_feature.SetField(
                STATISTICS_TABLE_FIELD_OPP_MAAIVELD,self.calculate_intersection_area(it_layer, new_feature,"maaiveld")
            )
            
            new_feature.SetField(
                STATISTICS_TABLE_FIELD_PERC_GEMENGD,round((100*new_feature[STATISTICS_TABLE_FIELD_OPP_GEMENGD]/new_feature[STATISTICS_TABLE_FIELD_OPP_TOTAAL]),2)
            )
            new_feature.SetField(
                STATISTICS_TABLE_FIELD_PERC_HWA,round((100*new_feature[STATISTICS_TABLE_FIELD_OPP_HWA]/new_feature[STATISTICS_TABLE_FIELD_OPP_TOTAAL]),2)
            )
            new_feature.SetField(
                STATISTICS_TABLE_FIELD_PERC_VGS,round((100*new_feature[STATISTICS_TABLE_FIELD_OPP_VGS]/new_feature[STATISTICS_TABLE_FIELD_OPP_TOTAAL]),2)
            )
            new_feature.SetField(
                STATISTICS_TABLE_FIELD_PERC_DWA,round((100*new_feature[STATISTICS_TABLE_FIELD_OPP_DWA]/new_feature[STATISTICS_TABLE_FIELD_OPP_TOTAAL]),2)
            )
            new_feature.SetField(
                STATISTICS_TABLE_FIELD_PERC_INFIL,round((100*new_feature[STATISTICS_TABLE_FIELD_OPP_INFIL]/new_feature[STATISTICS_TABLE_FIELD_OPP_TOTAAL]),2)
            )
            new_feature.SetField(
                STATISTICS_TABLE_FIELD_PERC_OPEN_WATER,round((100*new_feature[STATISTICS_TABLE_FIELD_OPP_OPEN_WATER]/new_feature[STATISTICS_TABLE_FIELD_OPP_TOTAAL]),2)
            )
            new_feature.SetField(
                STATISTICS_TABLE_FIELD_PERC_MAAIVELD,round((100*new_feature[STATISTICS_TABLE_FIELD_OPP_MAAIVELD]/new_feature[STATISTICS_TABLE_FIELD_OPP_TOTAAL]),2)
            )

            dest_layer.CreateFeature(new_feature)
            new_feature = None  # Dereference the feature to avoid memory leaks
        
        stats_ds = None
        it_layer = None

    def calculate_intersection_area(self,layer, stats_feature, stat_type):
        area_tot = 0
        area_gemengd = 0
        area_hwa = 0
        area_vgs = 0
        area_dwa = 0
        area_infil = 0
        area_open_water = 0
        area_maaiveld = 0
        
        # Get the geometry of the new feature
        stats_geom = stats_feature.GetGeometryRef()
    
        # Loop through all features in the layer
        for it_feature in layer:
            it_geom = it_feature.GetGeometryRef()
            
            # Validate the existing geometry
            if not it_geom.IsValid():
                it_geom = it_geom.MakeValid()
            
            if not it_geom or not stats_geom or not it_geom.IsValid() or not stats_geom.IsValid():
                continue
            
            # Check if the geometries intersect
            if stats_geom.Intersects(it_geom):
                try:
                    # Calculate the intersection
                    intersection_geom = stats_geom.Intersection(it_geom)
                    intersection_area = intersection_geom.GetArea()
                    
                    # Accumulate the total areas
                    area_tot += intersection_area
                    area_gemengd += intersection_area * it_feature[TARGET_TYPE_GEMENGD_RIOOL]/100
                    area_hwa += intersection_area * it_feature[TARGET_TYPE_HEMELWATERRIOOL]/100
                    area_vgs += intersection_area * it_feature[TARGET_TYPE_VGS_HEMELWATERRIOOL]/100
                    area_dwa += intersection_area * it_feature[TARGET_TYPE_VUILWATERRIOOL]/100
                    area_infil += intersection_area * it_feature[TARGET_TYPE_INFILTRATIEVOORZIENING]/100
                    area_open_water += intersection_area * it_feature[TARGET_TYPE_OPEN_WATER]/100
                    area_maaiveld += intersection_area * it_feature[TARGET_TYPE_MAAIVELD]/100
                
                except Exception as e:
                    print(f"Error calculating intersection: {e}")
                    continue
    
        # Return the calculated area based on the type
        if stat_type == "total":
            return round(area_tot/10000,2)
        elif stat_type == "gemengd":
            return round(area_gemengd/10000,2)
        elif stat_type == "hwa":
            return round(area_hwa/10000,2)
        elif stat_type == "vgs":
            return round(area_vgs/10000,2)
        elif stat_type == "dwa":
            return round(area_dwa/10000,2)
        elif stat_type == "infil":
            return round(area_infil/10000,2)
        elif stat_type == "open_water":
            return round(area_open_water/10000,2)
        elif stat_type == "maaiveld":
            return round(area_maaiveld/10000,2)

class Database:
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
        self.create_table(
            table_name=SETTINGS_TABLE_NAME, table_schema=SETTINGS_TABLE_SCHEMA
        ) #TO DO: WANNEER SETTINGS AL BESTAAN --> overnemen uit bestaande gpkg (bij het vullen, dit is alleen om de structuur aan te maken)
        self.create_table(
            table_name=STATISTICS_TABLE_NAME, table_schema=STATISTICS_TABLE_SCHEMA
        )
        
    @property
    def result_table(self):
        """Get reference to result layer (BGT Inlooptabel)
        :rtype ogr.Layer
        """
        return self.mem_database.GetLayerByName(RESULT_TABLE_NAME)
    
    @property
    def settings_table(self):
        """Get reference to the Settings layer
        :rtype ogr.Layer
        """
        return self.mem_database.GetLayerByName(SETTINGS_TABLE_NAME)
    
    @property
    def statistics_table(self):
        """Get reference to the Settings layer
        :rtype ogr.Layer
        """
        return self.mem_database.GetLayerByName(STATISTICS_TABLE_NAME)

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
            table_name, self.srs, geom_type=table_schema.geometry_type
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
                        self.mem_database.CopyLayer(src_layer=src_layer, new_name=stype)
                        print(
                            f"raw import of {stype} layer has {self.mem_database.GetLayerByName(stype).GetFeatureCount()} features"
                        )
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
            layer = self.mem_database.GetLayerByName(surface_type)
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
        """Merge and standardize all imported surfaces to one layer"""
        self.create_table(
            table_name=SURFACES_TABLE_NAME, table_schema=SURFACES_TABLE_SCHEMA
        )
        dest_layer = self.mem_database.GetLayerByName(SURFACES_TABLE_NAME)
        id_counter = 1
        previous_fcount = 0
        for stype in ALL_USED_SURFACE_TYPES:
            input_layer = self.mem_database.GetLayerByName(stype)
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
                target_geometry.AssignSpatialReference(self.srs)
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
    
    def _save_to_gpkg_test(self, file_path): #TO DO: weghalen, is alleen voor testen
        print("Preparing template gpkg")
        output_gpkg = r"C:\Users\ruben.vanderzaag\Documents\Github\bgt-inlooptool\QGIS_plugin\bgtinlooptool\style\output_bgtinlooptool_testing_rekeninstellingen.gpkg"

        print("Testen van output wegschrijven!!")
        self.out_db = GPKG_DRIVER.CopyDataSource(self.mem_database, output_gpkg)
        self.out_db = None
    
    def _save_to_gpkg(self, file_path):
        print("Preparing template gpkg")
        template_gpkg = r"C:\Users\ruben.vanderzaag\Documents\Github\bgt-inlooptool\QGIS_plugin\bgtinlooptool\style\template_output15.gpkg"
        output_gpkg = r"C:\Users\ruben.vanderzaag\Documents\Github\bgt-inlooptool\QGIS_plugin\bgtinlooptool\style\output_bgtinlooptool.gpkg"
        self.copy_and_rename_file(template_gpkg, output_gpkg)
        
        print("Saving Pipes layer in gpkg")
        db_layer = PIPES_TABLE_NAME #"pipes"
        gpkg_layer = "3. GWSW leidingen" 
        self._write_to_disk(file_path,db_layer, gpkg_layer)

        print("Saving BGT_inlooptabel layer in gpkg")
        db_layer =  "bgt_inlooptabel" #RESULT_TABLE_NAME
        gpkg_layer = "4. BGT inlooptabel"
        self._write_to_disk(file_path,db_layer, gpkg_layer)
        self.track_changes(file_path)
        
        print("Saving BGT_oppervlak layer in gpkg")
        db_layer = SURFACES_TABLE_NAME #"bgt_oppervlak"
        gpkg_layer = "5. BGT oppervlakken"
        self._write_to_disk(file_path,db_layer, gpkg_layer)

        print("Saving statistics layer in gpkg")
        db_layer = STATISTICS_TABLE_NAME 
        gpkg_layer = "6. Statistieken"
        self._write_to_disk(file_path,db_layer, gpkg_layer)
        
        print("Saving calculation settings in gpkg")
        db_layer = SETTINGS_TABLE_NAME 
        gpkg_layer = "7. Rekeninstellingen"
        self._write_to_disk(file_path,db_layer, gpkg_layer)

    
    def copy_and_rename_file(self,original_file_path, new_file_path):
        """
        Copies a file and renames the copy using only sys and os modules.

        :param original_file_path: Path to the original file.
        :param new_file_path: Path where the new file will be saved.
        """
        try:
            # Read the contents of the original file
            with open(original_file_path, 'rb') as original_file:
                content = original_file.read()

            # Write the contents to the new file
            with open(new_file_path, 'wb') as new_file:
                new_file.write(content)

            print(f"File copied from {original_file_path} to {new_file_path}")
        except FileNotFoundError:
            print(f"The file {original_file_path} does not exist.")
        except PermissionError:
            print(f"Permission denied. Unable to copy {original_file_path} to {new_file_path}.")
        except Exception as e:
            print(f"An error occurred: {e}")
            
    def _write_to_disk(self, file_path, db_layer_name, dst_layer_name): 
        """Copy self.mem_database to file_path"""
        # Get the source layer from the memory database
        self.db_layer = self.mem_database.GetLayerByName(db_layer_name)
        if self.db_layer is None:
            raise ValueError(f"Layer '{db_layer_name}' not found in memory database.")
        
        # Open the destination GeoPackage in write mode
        self.dst_gpkg = GPKG_DRIVER.Open(file_path, 1)  # 1 means writable
        if self.dst_gpkg is None:
            raise ValueError(f"Could not open GeoPackage '{file_path}' for writing.")
        
        # Get the destination layer from the GeoPackage
        self.dst_layer = self.dst_gpkg.GetLayerByName(dst_layer_name)
        if self.dst_layer is None:
            raise ValueError(f"Layer '{dst_layer_name}' not found in destination GeoPackage.")
        
        # Get the layer definitions for both the source and destination layers
        layer_defn = self.db_layer.GetLayerDefn()
        dst_layer_defn = self.dst_layer.GetLayerDefn()
        
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
        for feature in self.db_layer:
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
            self.dst_layer.CreateFeature(dst_feature)
            dst_feature = None  # Free resources
        # Clean up
        self.dst_gpkg = None
        self.dst_layer = None
        self.db_layer = None
        print("Done with saving")

    def track_changes(self, file_path):
        # Add SQL triggers to track changes

        # Open the GeoPackage
        ds = ogr.Open(file_path, update=True)
        
        # SQL statements to create the triggers
        sql_time_last_change = """
        CREATE TRIGGER update_laaste_wijziging_on_update AFTER UPDATE
        OF bgt_identificatie, type_verharding, graad_verharding, hellingstype, hellingspercentage, type_private_voorziening, berging_private_voorziening, code_voorziening, putcode, leidingcode, gemengd_riool, hemelwaterriool, vgs_hemelwaterriool, vuilwaterriool, infiltratievoorziening, open_water, maaiveld
        ON "4. BGT inlooptabel"
        FOR EACH ROW
        BEGIN
        UPDATE "4. BGT inlooptabel" SET laatste_wijziging = CURRENT_TIMESTAMP WHERE id = old.id;
        END 
        """
        
        sql_changed_tf = """
        CREATE TRIGGER update_wijziging_on_update AFTER UPDATE
        OF bgt_identificatie, type_verharding, graad_verharding, hellingstype, hellingspercentage, type_private_voorziening, berging_private_voorziening, code_voorziening, putcode, leidingcode, gemengd_riool, hemelwaterriool, vgs_hemelwaterriool, vuilwaterriool, infiltratievoorziening, open_water, maaiveld
        ON "4. BGT inlooptabel"
        FOR EACH ROW
        BEGIN
        UPDATE "4. BGT inlooptabel" SET wijziging = 1 WHERE id = old.id;
        END
        """
        
        # Execute the SQL statements
        ds.ExecuteSQL(sql_time_last_change)
        ds.ExecuteSQL(sql_changed_tf)

        # Close the data source
        ds = None

        print("Triggers created successfully.")

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


if __name__ == "__main__":
    pass
