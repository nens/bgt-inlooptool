# System imports
import os
import sys
import contextlib

# Third-party imports
from osgeo import osr
from osgeo import gdal
from osgeo import ogr
from datetime import datetime

try: # Rtree should be installed by the plugin for QGIS
    import rtree
except ImportError:
    try:
        import subprocess
        command = ["python", "-m", "pip", "install", "rtree"]
        result = subprocess.run(command, capture_output=True, text=True)
        import rtree
    except: # For ArcGIS Pro the following is needed
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
        leidingcodes_koppelen=KOPPEL_LEIDINGCODES,
        gebruik_bag=GEBRUIK_BAG,
        gebruik_kolken=GEBRUIK_KOLKEN,
        gebruik_resultaten=GEBRUIK_RESULTATEN,
        gebruik_statistieken=GEBRUIK_STATISTIEKEN,
        download_bgt=DOWNLOAD_BGT,
        download_gwsw=DOWNLOAD_GWSW,
        download_bag=DOWNLOAD_BAG,
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
        self.leidingcodes_koppelen = leidingcodes_koppelen
        self.gebruik_bag = gebruik_bag
        self.gebruik_kolken = gebruik_kolken
        self.gebruik_resultaten = gebruik_resultaten
        self.gebruik_statistieken = gebruik_statistieken
        self.download_bgt = download_bgt
        self.download_gwsw = download_gwsw
        self.download_bag = download_bag
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
        self.inf_pavements_green_roof_surfaces = []
        self.relative_hoogteligging_surfaces = []
        self.new_BGT_surfaces = []
        self.outdated_changed_surfaces = []
        
    def set_settings_start(self,bgt_file,pipe_file,building_file, kolken_file):
        settings_table = self._database.settings_table
        feature_defn = settings_table.GetLayerDefn()
        feature = ogr.Feature(feature_defn)

        # Copy settings from previous runs to the new settings table:
        prev_settings = self._database.mem_database.GetLayerByName(SETTINGS_TABLE_NAME_PREV)
        
        if prev_settings is not None:
            self._database.copy_features_with_matching_fields(prev_settings,settings_table,"run_id")

        max_fid = -1
        for feature in settings_table:
            fid = feature.GetFID()+1
            if fid > max_fid:
                max_fid = fid
        
        if feature is None: 
            new_fid = 1
        else:
            new_fid = max_fid + 1

        feature.SetField(
            SETTINGS_TABLE_FIELD_ID,
            new_fid,
        )
        feature.SetField(
            SETTINGS_TABLE_FIELD_TIJD_START,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        feature.SetField(
            SETTINGS_TABLE_FIELD_DOWNLOAD_BGT, self.parameters.download_bgt
        )
        feature.SetField(
            SETTINGS_TABLE_FIELD_DOWNLOAD_GWSW, self.parameters.download_gwsw
        )
        feature.SetField(
            SETTINGS_TABLE_FIELD_DOWNLOAD_BAG, self.parameters.download_bag
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
        feature.SetField(
            SETTINGS_TABLE_FIELD_LEIDINGCODES_KOPPELEN, self.parameters.leidingcodes_koppelen
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
            
            # Clean up
            feature_to_update = None
            settings_table = None
            print(f"Settings of run {max_fid} updated successfully.")
        else:
            print("No features found in the layer.")
    
    def import_results(self,file_path):
        """
        Import results from previous run to _database
        :param file_path: path to results gpkg of a previous run
        :return: None
        """
        self._database.import_settings_results(file_path)
        self._database.import_inf_pavement_green_roofs(file_path)
        self._database.import_it_results(file_path)
        self._database.clean_it_results()
        
    def import_surfaces(self, file_path,extent_wkt):
        """
        Import BGT Surfaces to _database
        :param file_path: path to bgt zip file
        :return: None
        """
        self._database.import_surfaces_raw(file_path,extent_wkt)
        self._database.clean_surfaces()
        self._database.merge_surfaces()
        self._database.classify_surfaces(self.parameters)
        self.relative_hoogteligging_surfaces = self._database.identify_overlapping_surfaces()

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
        #print(f"surface_water_buffer_dist: {surface_water_buffer_dist}")
        
        # Distance to pipes
        for surface in self._database.bgt_surfaces:
            if not surface:
                print("surface invalid")
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
                            distances[internal_pipe_type] = {"distance": pipe_geom.Distance(surface_geom),
                                                             "leidingcode": pipe["naam"]
                                                             }
                        else:
                            if distances[internal_pipe_type]["distance"] > pipe_geom.Distance(
                                surface_geom
                            ):
                                distances[internal_pipe_type] = {"distance": pipe_geom.Distance(surface_geom),
                                                                 "leidingcode": pipe["naam"]
                                                                 }
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
                distances[OPEN_WATER] = {"distance": min_water_distance,
                                         "leidingcode": None
                                         }
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
                    distances[KOLK] = {"distance": min_kolk_distance,
                                             "leidingcode": None
                                             }
            # Write distances to surfaces layer
            for distance_type in DISTANCE_TYPES:

                if distance_type in distances:
                    if distances[distance_type]["distance"] == PSEUDO_INFINITE:
                        distances[distance_type]["distance"] = None
                    surface["distance_" + distance_type] = distances[distance_type]["distance"]
                    surface["code_"+ distance_type] = distances[distance_type]["leidingcode"]

            self._database.bgt_surfaces.SetFeature(surface)
            surface = None
        self._database.bgt_surfaces.ResetReading()
        self._database.bgt_surfaces.SetSpatialFilter(None)

    def calculate_runoff_targets(self,leidingcode_koppelen):
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
                "bgt_fysiek_voorkomen", surface.bgt_fysiek_voorkomen 
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
            if leidingcode_koppelen:
                if feature.GetField(TARGET_TYPE_GEMENGD_RIOOL) > 0:
                    feature.SetField(RESULT_TABLE_FIELD_CODE_GEMENGD, surface["code_" + INTERNAL_PIPE_TYPE_GEMENGD_RIOOL])
                if feature.GetField(TARGET_TYPE_HEMELWATERRIOOL) > 0 or feature.GetField(TARGET_TYPE_VGS_HEMELWATERRIOOL) > 0:
                    if feature.GetField(TARGET_TYPE_HEMELWATERRIOOL) >feature.GetField(TARGET_TYPE_VGS_HEMELWATERRIOOL):
                        feature.SetField(RESULT_TABLE_FIELD_CODE_HWA, surface["code_" + INTERNAL_PIPE_TYPE_HEMELWATERRIOOL])
                    else:
                        feature.SetField(RESULT_TABLE_FIELD_CODE_HWA, surface["code_" + INTERNAL_PIPE_TYPE_VGS_HEMELWATERRIOOL])
                if feature.GetField(TARGET_TYPE_VUILWATERRIOOL) > 0:
                    feature.SetField(RESULT_TABLE_FIELD_CODE_DWA, surface["code_" + INTERNAL_PIPE_TYPE_VUILWATERRIOOL])
                if feature.GetField(TARGET_TYPE_INFILTRATIEVOORZIENING) > 0:
                    feature.SetField(RESULT_TABLE_FIELD_CODE_INFILTRATIE, surface["code_" + INTERNAL_PIPE_TYPE_INFILTRATIEVOORZIENING])
        
            result_table.CreateFeature(feature)
            feature = None

    def get_nearest_pipe_code(self,feature):
        surface_geom = feature.geometry().Clone()
        surface_geom_buffer_afwateringsvoorziening = surface_geom.Buffer(
            self.parameters.max_afstand_vlak_afwateringsvoorziening
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
                        distances[internal_pipe_type] = {"distance": pipe_geom.Distance(surface_geom),
                                                         "leidingcode": pipe["naam"]
                                                         }
                    else:
                        if distances[internal_pipe_type]["distance"] > pipe_geom.Distance(
                            surface_geom
                        ):
                            distances[internal_pipe_type] = {"distance": pipe_geom.Distance(surface_geom),
                                                             "leidingcode": pipe["naam"]
                                                             }
        pipe = None
        return distances                    
    
    def overwrite_by_manual_edits(self,leidingcodes_koppelen):
        result_table = self._database.result_table
        manual_results_prev = self._database.mem_database.GetLayerByName(RESULT_TABLE_NAME_PREV)
        bgt_surfaces = self._database.bgt_surfaces
    
        if manual_results_prev is None:
            print("No manual edits to keep.")
            return
        
        records_to_delete = []
        features_to_update = []
    
        # Iterate over each feature in manual_results_prev
        for count, prev_feat in enumerate(manual_results_prev, 1):
            if leidingcodes_koppelen:
                distances = self.get_nearest_pipe_code(prev_feat)
        
                # Assign the correct code based on the type of the pipe
                if prev_feat.GetField(TARGET_TYPE_GEMENGD_RIOOL) > 0:
                    if INTERNAL_PIPE_TYPE_GEMENGD_RIOOL in distances:
                        prev_feat.SetField(RESULT_TABLE_FIELD_CODE_GEMENGD, distances[INTERNAL_PIPE_TYPE_GEMENGD_RIOOL]["leidingcode"])
                    else:
                        print(f"No mixed sewerage pipe found for prev_feat {prev_feat.GetFID()}")
        
                elif (prev_feat.GetField(TARGET_TYPE_HEMELWATERRIOOL) > 0 or prev_feat.GetField(TARGET_TYPE_VGS_HEMELWATERRIOOL) > 0):
                    if prev_feat.GetField(TARGET_TYPE_HEMELWATERRIOOL) > prev_feat.GetField(TARGET_TYPE_VGS_HEMELWATERRIOOL):
                        if INTERNAL_PIPE_TYPE_HEMELWATERRIOOL in distances:
                            prev_feat.SetField(RESULT_TABLE_FIELD_CODE_HWA, distances[INTERNAL_PIPE_TYPE_HEMELWATERRIOOL]["leidingcode"])
                        else:
                            print(f"No rainwater pipe found for prev_feat {prev_feat.GetFID()}")
                    elif INTERNAL_PIPE_TYPE_VGS_HEMELWATERRIOOL in distances:
                        prev_feat.SetField(RESULT_TABLE_FIELD_CODE_HWA, distances[INTERNAL_PIPE_TYPE_VGS_HEMELWATERRIOOL]["leidingcode"])
                    else:
                        print(f"No VGS rainwater pipe found for prev_feat {prev_feat.GetFID()}")
        
                elif prev_feat.GetField(TARGET_TYPE_VUILWATERRIOOL) > 0:
                    if INTERNAL_PIPE_TYPE_VUILWATERRIOOL in distances:
                        prev_feat.SetField(RESULT_TABLE_FIELD_CODE_DWA, distances[INTERNAL_PIPE_TYPE_VUILWATERRIOOL]["leidingcode"])
                    else:
                        print(f"No waste water pipe found for prev_feat {prev_feat.GetFID()}")
        
                elif prev_feat.GetField(TARGET_TYPE_INFILTRATIEVOORZIENING) > 0:
                    if INTERNAL_PIPE_TYPE_INFILTRATIEVOORZIENING in distances:
                        prev_feat.SetField(RESULT_TABLE_FIELD_CODE_INFILTRATIE, distances[INTERNAL_PIPE_TYPE_INFILTRATIEVOORZIENING]["leidingcode"])
                    else:
                        print(f"No infiltration pipe found for prev_feat {prev_feat.GetFID()}")
    
            # Collect the features for batch processing
            features_to_update.append(prev_feat)
    
            # Mark records in result_table for deletion based on matching key field
            key_value = prev_feat.GetField("bgt_identificatie")
            result_table.SetAttributeFilter(f"bgt_identificatie = '{key_value}'")
            for result_feat in result_table:
                records_to_delete.append(result_feat.GetFID())
            result_table.SetAttributeFilter(None)  # Clear the filter for next iteration
    
        # Batch delete records
        if records_to_delete:
            for fid in records_to_delete:
                result_table.DeleteFeature(fid)

        # Batch update manual_results_prev in result_table
        if features_to_update:
            for feat in features_to_update:
                manual_results_prev.SetFeature(feat)
    
            # Copy features from manual_results_prev to result_table
            self._database.copy_features_with_matching_fields(manual_results_prev, result_table, "id")
    
        # Sync the changes to disk
        result_table.SyncToDisk()
        
        # Check if the manual edits overlap with new BGT feature (for more than 50% of its own surface)          
        for prev_feat in manual_results_prev:
            #intersecting_fids = []
            overlapping_area = 0
            #calculate area of prev_feat
            prev_feat_geom = prev_feat.GetGeometryRef()
            area_prev_feat = prev_feat_geom.GetArea()
            for surface in bgt_surfaces:
                surface_geom = surface.GetGeometryRef()
                if surface_geom.Intersects(prev_feat_geom) and (prev_feat["bgt_identificatie"]!= surface["identificatie_lokaalid"]):
                    intersection = surface_geom.Intersection(prev_feat_geom)
                    if intersection:
                        overlapping_area += intersection.GetArea()
            
            if area_prev_feat > 0 and (overlapping_area/area_prev_feat > 0.5): 
                self.new_BGT_surfaces.append(prev_feat)  
            
            # Check if the manual edits have an eindregistratie (and are therefor old BGT features)    
            surfaces_ids = []
            for surface in bgt_surfaces:
                surfaces_ids.append(surface.GetField("identificatie_lokaalid"))
            
            if prev_feat["bgt_identificatie"] not in surfaces_ids:
                self.outdated_changed_surfaces.append(prev_feat)
        
    
    def intersect_inf_pavement_green_roofs(self):
        result_table = self._database.result_table
        points_layer = self._database.mem_database.GetLayerByName(INF_PAVEMENT_TABLE_NAME_PREV)
        
        # Iterate over features in the points_layer
        if points_layer is None:
            print("No infiltrating pavement or green roofs specified.")
        else:
            for point_feature in points_layer:
                point_geom = point_feature.GetGeometryRef()  # Get the geometry of the current point feature
                
                # Get the value of the 'type' field for the current point feature
                feature_type = point_feature.GetField("type")
                
                # Iterate over features in the result_table
                for result_feature in result_table:
                    result_geom = result_feature.GetGeometryRef()  # Get the geometry of the current result feature
                    
                    # Check if the geometries intersect
                    if result_geom.Intersects(point_geom):
                        # Update the 'surface_type' field based on the 'type' field from the point layer
                        if feature_type == "Waterpasserende verharding":
                            result_feature.SetField(RESULT_TABLE_FIELD_TYPE_VERHARDING, VERHARDINGSTYPE_WATERPASSEREND_VERHARD)
                        elif feature_type == "Groen dak":
                            result_feature.SetField(RESULT_TABLE_FIELD_TYPE_VERHARDING, VERHARDINGSTYPE_GROEN_DAK)
                        
                        # Update the feature in the result table
                        result_table.SetFeature(result_feature)
                        self.inf_pavements_green_roof_surfaces.append(result_feature)

    def calculate_statistics(self, stats_path):
        dest_layer = self._database.statistics_table
        stats_abspath = os.path.abspath(stats_path)
        it_layer = self._database.result_table
        
        if not os.path.isfile(stats_abspath):
            raise FileNotFoundError(f"Shapefile met gebieden voor statistieken niet gevonden: {stats_abspath}")
        
        stats_ds = ogr.Open(stats_abspath)
        stats_layer = stats_ds.GetLayer()
        gebied_id = 0
        field_prefix = ["opp", "perc"]
        field_middle = ["_totaal", "_gemengd", "_hwa", "_vgs", "_dwa", "_infiltratievoorziening", "_open_water", "_maaiveld"]
        field_suffix = ["", "_dak", "_gesl_verh", "_open_verh", "_onverhard"]
        field_suffix_verharding = ["_dak","_gesl_verh","_open_verh","_onverhard","_groen_dak","_waterpas_verh","_water"]
    
        for feature in stats_layer:
            gebied_id += 1
            geom = feature.GetGeometryRef()
            new_feature = ogr.Feature(dest_layer.GetLayerDefn())
            new_feature.SetGeometry(geom.Clone())
            new_feature.SetField(STATISTICS_TABLE_FIELD_ID, gebied_id)
            
            intersecting_it_features = self.find_indices_intersecting_features(it_layer,new_feature)
            
            intersection_areas = {}
            
            for prefix in field_prefix:
                for middle in field_middle:
                    middle_key = middle[1:]
                    if prefix == "opp":
                        for suffix in field_suffix:
                            field_name = ("STATISTICS_TABLE_FIELD_" + prefix + middle + suffix).upper()
                            if field_name not in intersection_areas:
                                intersection_areas[field_name] = self.calculate_intersection_area(intersecting_it_features, new_feature, middle_key, suffix[1:])
                            new_feature.SetField(globals()[field_name], intersection_areas[field_name])
                    else:
                        for suffix in field_suffix:
                            if middle_key != "totaal":
                                field_name = ("STATISTICS_TABLE_FIELD_" + prefix + middle + suffix).upper()
                                field_name_opp = field_name.replace("PERC", "OPP")
                                field_name_tot = field_name_opp.replace(middle_key.upper(), "TOTAAL")
                                if new_feature[globals()[field_name_tot]] > 0:
                                    perc_value = round((100 * new_feature[globals()[field_name_opp]] / new_feature[globals()[field_name_tot]]), 2)
                                    new_feature.SetField(globals()[field_name], perc_value)

            for prefix in field_prefix:
                for suffix_verharding in field_suffix_verharding:
                    field_name = ("STATISTICS_TABLE_FIELD_" + prefix + suffix_verharding).upper()
                    if prefix == "opp":
                        if field_name not in intersection_areas:
                            intersection_areas[field_name] = self.calculate_intersection_area(intersecting_it_features, new_feature, "verharding", suffix_verharding[1:])
                        new_feature.SetField(globals()[field_name], intersection_areas[field_name])
                    else:
                        field_name_opp = field_name.replace("PERC", "OPP")
                        field_name_tot = field_name_opp.replace(suffix_verharding[1:].upper(), "TOTAAL")
                        if new_feature[globals()[field_name_tot]] > 0:
                            perc_value = round((100 * new_feature[globals()[field_name_opp]] / new_feature[globals()[field_name_tot]]), 2)
                            new_feature.SetField(globals()[field_name], perc_value)
    
            dest_layer.CreateFeature(new_feature)
            new_feature = None

    
        stats_ds = None
        it_layer = None
    
    def find_indices_intersecting_features(self, layer, stats_feature):
        """
        Returns a list of feature IDs (FIDs) of all features in 'layer' that intersect with 'stats_feature'.
        
        Parameters:
            layer (ogr.Layer): The layer to check for intersecting features.
            stats_feature (ogr.Feature): The feature to check intersections against.
        
        Returns:
            List[int]: List of feature IDs (FIDs) in 'layer' that intersect with 'stats_feature'.
        """
        intersecting_fids = []
        
        # Get the geometry of the stats_feature to check intersections
        stats_geom = stats_feature.GetGeometryRef()
        
        # Loop through all features in the layer
        for feature in layer:
            feature_geom = feature.GetGeometryRef()
            
            # Check if the geometries intersect
            if feature_geom and stats_geom and feature_geom.Intersects(stats_geom):
                intersecting_fids.append(feature.GetFID())
        
        # Reset the reading for the layer to allow further use
        layer.ResetReading()
        
        return intersecting_fids

    def calculate_intersection_area(self, intersecting_it_features, stats_feature, stat_type, type_verharding):
        it_layer = self._database.result_table
        area_totals = {
            "totaal": 0,
            "gemengd": 0,
            "hwa": 0,
            "vgs": 0,
            "dwa": 0,
            "infiltratievoorziening": 0,
            "open_water": 0,
            "maaiveld": 0,
            "verharding": 0
        }
        
        stats_geom = stats_feature.GetGeometryRef()
        verhardingstype_map = {
            "gesl_verh": VERHARDINGSTYPE_GESLOTEN_VERHARD,
            "open_verh": VERHARDINGSTYPE_OPEN_VERHARD,
            "groen_dak": VERHARDINGSTYPE_GROEN_DAK,
            "waterpas_verh": VERHARDINGSTYPE_WATERPASSEREND_VERHARD,
        }
        verhardingstype = verhardingstype_map.get(type_verharding, type_verharding)
        
        if not stats_geom.IsValid():
            stats_geom = stats_geom.MakeValid()
        
        for fid in intersecting_it_features:
            it_feature = it_layer.GetFeature(fid)
            it_geom = it_feature.GetGeometryRef()
            
            if not it_geom.IsValid():
                it_geom = it_geom.MakeValid()
            
            if it_feature[RESULT_TABLE_FIELD_TYPE_VERHARDING] == verhardingstype or verhardingstype == "":
                if it_geom and stats_geom and it_geom.IsValid() and stats_geom.IsValid() and stats_geom.Intersects(it_geom):
                    try:
                        intersection_geom = stats_geom.Intersection(it_geom)
                        intersection_area = intersection_geom.GetArea()
                        area_totals["totaal"] += intersection_area
                        area_totals["verharding"] += intersection_area
                        area_totals["gemengd"] += intersection_area * it_feature[TARGET_TYPE_GEMENGD_RIOOL] / 100
                        area_totals["hwa"] += intersection_area * it_feature[TARGET_TYPE_HEMELWATERRIOOL] / 100
                        area_totals["vgs"] += intersection_area * it_feature[TARGET_TYPE_VGS_HEMELWATERRIOOL] / 100
                        area_totals["dwa"] += intersection_area * it_feature[TARGET_TYPE_VUILWATERRIOOL] / 100
                        area_totals["infiltratievoorziening"] += intersection_area * it_feature[TARGET_TYPE_INFILTRATIEVOORZIENING] / 100
                        area_totals["open_water"] += intersection_area * it_feature[TARGET_TYPE_OPEN_WATER] / 100
                        area_totals["maaiveld"] += intersection_area * it_feature[TARGET_TYPE_MAAIVELD] / 100
                    except Exception as e:
                        print(f"Error calculating intersection: {e}")
                        continue
        
        return round(area_totals[stat_type] / 10000, 2) 
    
    def generate_warnings(self): 
        checks_table = self._database.checks_table
        it_layer = self._database.result_table
        feature_defn = checks_table.GetLayerDefn()
        #print(feature_defn)
        fid = 0
        
        #Check 1: large areas
        warning_large_area = f"Dit BGT vlak is groter dan {CHECKS_LARGE_AREA} m2. De kans is groot dat dit vlak aangesloten is op meerdere stelseltypen. Controleer en corrigeer dit wanneer nodig."
        
        for it_feature in it_layer:
            # Get the geometry of the feature and calculate area
            geom = it_feature.GetGeometryRef()
            area = geom.GetArea()
            if area > CHECKS_LARGE_AREA: # value in m2
                fid += 1
                check_feature = ogr.Feature(feature_defn)
                check_feature.SetGeometry(geom.Clone())
                check_feature.SetField(CHECKS_TABLE_FIELD_ID,fid)
                check_feature.SetField(CHECKS_TABLE_FIELD_LEVEL, "Waarschuwing")
                check_feature.SetField(CHECKS_TABLE_FIELD_CODE,1)
                check_feature.SetField(CHECKS_TABLE_FIELD_TABLE,"4. BGT inlooptabel")
                check_feature.SetField(CHECKS_TABLE_FIELD_COLUMN,"")
                check_feature.SetField(CHECKS_TABLE_FIELD_VALUE,str(round(area,2)))
                check_feature.SetField(CHECKS_TABLE_FIELD_DESCRIPTION,warning_large_area)
                checks_table.CreateFeature(check_feature)
                check_feature = None  # Cleanup after creating the feature
                
        #Check 2: buildings that are in the BGT but not in the BAG
        warning_bgt_bag_mismatch = "Dit pand komt wel voor in de BGT, maar niet in de BAG. Er is daarom geen bouwjaar toegewezen aan het pand."
        
        for building in self._database.non_matching_buildings:
            fid += 1
            geom = building.GetGeometryRef()
            check_feature = ogr.Feature(feature_defn)
            check_feature.SetGeometry(geom.Clone())
            check_feature.SetField(CHECKS_TABLE_FIELD_ID,fid)
            check_feature.SetField(CHECKS_TABLE_FIELD_LEVEL, "Info")
            check_feature.SetField(CHECKS_TABLE_FIELD_CODE,2)
            check_feature.SetField(CHECKS_TABLE_FIELD_TABLE,"4. BGT inlooptabel")
            check_feature.SetField(CHECKS_TABLE_FIELD_COLUMN,"BGT Identificatie")
            check_feature.SetField(CHECKS_TABLE_FIELD_VALUE,building["identificatie_lokaalid"])   #identificatiebagpnd
            check_feature.SetField(CHECKS_TABLE_FIELD_DESCRIPTION,warning_bgt_bag_mismatch
                                   )
            checks_table.CreateFeature(check_feature)
            check_feature = None  # Cleanup after creating the feature
        
        #Check 3: surface which intersect with green roofs or infiltrating pavement
        warning_infiltrating_surfaces = "Dit vlak is waterpasserende verharding of een groen dak. Het type verharding is daarop aangepast, maar de percentuele afwatering nog niet."
        
        for surface in self.inf_pavements_green_roof_surfaces:
            fid += 1
            geom = surface.GetGeometryRef()
            check_feature = ogr.Feature(feature_defn)
            check_feature.SetGeometry(geom.Clone())
            check_feature.SetField(CHECKS_TABLE_FIELD_ID,fid)
            check_feature.SetField(CHECKS_TABLE_FIELD_LEVEL, "Info")
            check_feature.SetField(CHECKS_TABLE_FIELD_CODE,3)
            check_feature.SetField(CHECKS_TABLE_FIELD_TABLE,"4. BGT inlooptabel")
            check_feature.SetField(CHECKS_TABLE_FIELD_COLUMN,"Type verharding")
            check_feature.SetField(CHECKS_TABLE_FIELD_VALUE,surface["type_verharding"])
            check_feature.SetField(CHECKS_TABLE_FIELD_DESCRIPTION,warning_infiltrating_surfaces
                                   )
            checks_table.CreateFeature(check_feature)
            check_feature = None  # Cleanup after creating the feature
        
        #Check 4: relatieve hoogteligging 
        warning_relatieve_hoogteligging = "Dit vlak overlapt met een ander BGT vlak en heeft een hogere relatieve hoogteligging. Neerslag valt op het vlak met de hoogste relatieve hoogteligging. Zorg dat er geen overlap is tussen de vlakken en alleen de vlakken met hoogste relatieve hoogteligging in de dataset zitten."
        
        for surface in self.relative_hoogteligging_surfaces:
            fid += 1
            geom = surface.GetGeometryRef()
            check_feature = ogr.Feature(feature_defn)
            check_feature.SetGeometry(geom.Clone())
            check_feature.SetField(CHECKS_TABLE_FIELD_ID,fid)
            check_feature.SetField(CHECKS_TABLE_FIELD_LEVEL, "Waarschuwing")
            check_feature.SetField(CHECKS_TABLE_FIELD_CODE,4)
            check_feature.SetField(CHECKS_TABLE_FIELD_TABLE,"5. BGT oppervlakken")
            check_feature.SetField(CHECKS_TABLE_FIELD_COLUMN,"BGT Identificatie")
            check_feature.SetField(CHECKS_TABLE_FIELD_VALUE,surface["identificatie_lokaalid"])
            check_feature.SetField(CHECKS_TABLE_FIELD_DESCRIPTION,warning_relatieve_hoogteligging
                                   )
            checks_table.CreateFeature(check_feature)
            check_feature = None  # Cleanup after creating the feature
        
        #Check 5: nieuwe vlakken in de BGT, met nieuwe IDs, dan kunnen deze overlappen met de handmatige wijzigingen. 
        warning_new_BGT_surfaces = "Dit handmatige gewijzigde vlak heeft meer dan 50% overlap met een nieuw BGT vlak. Controleer of dit vlak behouden moet blijven."
        for it_feature in self.new_BGT_surfaces:
            fid += 1
            geom = it_feature.GetGeometryRef()
            check_feature = ogr.Feature(feature_defn)
            check_feature.SetGeometry(geom.Clone())
            check_feature.SetField(CHECKS_TABLE_FIELD_ID,fid)
            check_feature.SetField(CHECKS_TABLE_FIELD_LEVEL, "Waarschuwing")
            check_feature.SetField(CHECKS_TABLE_FIELD_CODE,5)
            check_feature.SetField(CHECKS_TABLE_FIELD_TABLE,"4. BGT inlooptabel")
            check_feature.SetField(CHECKS_TABLE_FIELD_COLUMN,"BGT identificatie")
            check_feature.SetField(CHECKS_TABLE_FIELD_VALUE,it_feature["bgt_identificatie"])
            check_feature.SetField(CHECKS_TABLE_FIELD_DESCRIPTION,warning_new_BGT_surfaces
                                   )
            checks_table.CreateFeature(check_feature)
            check_feature = None  # Cleanup after creating the feature
        
        #Check 6: handmatig gewijzigd BGT vlak heeft een eindregistratie gekregen
        warning_outdated_changed_surfaces = "Dit handmatig gewijzigde vlak bestaat niet meer in de BGT data. Controleer of het nog steeds bestaat." 
        for it_feature in self.outdated_changed_surfaces:
            fid += 1
            geom = it_feature.GetGeometryRef()
            check_feature = ogr.Feature(feature_defn)
            check_feature.SetGeometry(geom.Clone())
            check_feature.SetField(CHECKS_TABLE_FIELD_ID,fid)
            check_feature.SetField(CHECKS_TABLE_FIELD_LEVEL, "Waarschuwing")
            check_feature.SetField(CHECKS_TABLE_FIELD_CODE,6)
            check_feature.SetField(CHECKS_TABLE_FIELD_TABLE,"4. BGT inlooptabel")
            check_feature.SetField(CHECKS_TABLE_FIELD_COLUMN,"BGT identificatie")
            check_feature.SetField(CHECKS_TABLE_FIELD_VALUE,it_feature["bgt_identificatie"])
            check_feature.SetField(CHECKS_TABLE_FIELD_DESCRIPTION,warning_outdated_changed_surfaces
                                   )
            checks_table.CreateFeature(check_feature)
            check_feature = None  # Cleanup after creating the feature
        
        checks_table = None
        it_layer = None

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
        )
        self.create_table(
            table_name=STATISTICS_TABLE_NAME, table_schema=STATISTICS_TABLE_SCHEMA
        )
        self.create_table(
            table_name=CHECKS_TABLE_NAME, table_schema=CHECKS_TABLE_SCHEMA
        )
        self.non_matching_buildings = []
        
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
    def checks_table(self):
        """Get reference to the Settings layer
        :rtype ogr.Layer
        """
        return self.mem_database.GetLayerByName(CHECKS_TABLE_NAME)

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
    
    def import_it_results(self, file_path):
        prev_gpkg_abspath = os.path.abspath(file_path)
        if not os.path.isfile(prev_gpkg_abspath):
            raise FileNotFoundError(
                "Resultaten GeoPackage vorige run niet gevonden: {}".format(prev_gpkg_abspath)
            )
        it_ds = ogr.Open(file_path)
        # TODO more thorough checks of validity of input geopackage
        try:
            self.mem_database.CopyLayer(
                it_ds.GetLayerByName("4. BGT inlooptabel"), RESULT_TABLE_NAME_PREV
            )
        except Exception:
            # TODO more specific exception
            raise FileInputError(
                "Ongeldige input: {} is geen geldige Resultaten GeoPackage".format(
                    prev_gpkg_abspath
                )
            )
    def clean_it_results(self):
        """
        Update the results layer from the previous simulation such that only the manual changes are kept.
        """
        layer = self.mem_database.GetLayerByName(RESULT_TABLE_NAME_PREV)
        if layer is None:
            raise DatabaseOperationError

        delete_fids = []
        for it_feat in layer:
            if not it_feat["wijziging"]:
                delete_fids.append(it_feat.GetFID())

        for fid in delete_fids:
            layer.DeleteFeature(fid)

        layer = None
        
    def import_settings_results(self, file_path):
        prev_gpkg_abspath = os.path.abspath(file_path)
        if not os.path.isfile(prev_gpkg_abspath):
            raise FileNotFoundError(
                "Resultaten GeoPackage vorige run niet gevonden: {}".format(prev_gpkg_abspath)
            )
        it_ds = ogr.Open(file_path)
        # TODO more thorough checks of validity of input geopackage
        try:
            self.mem_database.CopyLayer(
                it_ds.GetLayerByName("7. Rekeninstellingen"), SETTINGS_TABLE_NAME_PREV
            )
        except Exception:
            # TODO more specific exception
            raise FileInputError(
                "Ongeldige input: {} is geen geldige Resultaten GeoPackage".format(
                    prev_gpkg_abspath
                )
            )  
    
    def import_inf_pavement_green_roofs(self,file_path):
        prev_gpkg_abspath = os.path.abspath(file_path)
        if not os.path.isfile(prev_gpkg_abspath):
            raise FileNotFoundError(
                "Resultaten GeoPackage vorige run niet gevonden: {}".format(prev_gpkg_abspath)
            )
        it_ds = ogr.Open(file_path)
        # TODO more thorough checks of validity of input geopackage/shapefile
        try:
            self.mem_database.CopyLayer(
                it_ds.GetLayerByName("1. Waterpasserende verharding en groene daken [optionele input]"), INF_PAVEMENT_TABLE_NAME_PREV
            )
        except Exception:
            # TODO more specific exception
            raise FileInputError(
                "Ongeldige input: {} is geen geldige Resultaten GeoPackage".format(
                    prev_gpkg_abspath
                )
            )  
    
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

    def import_surfaces_raw(self, file_path,extent_wkt):
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
                        # Set spatial filter on src_layer to only include features that intersect with the extent
                        if extent_wkt is not None: 
                            extent_geometry = ogr.CreateGeometryFromWkt(extent_wkt)
                            src_layer.SetSpatialFilter(extent_geometry)
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
            #self.import_surfaces_raw_alternative(file_path)
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
                if geom is None:
                    # If no geometry is found, skip this feature
                    print(f"Warning: Feature {feature.GetFID()} in layer {surface_type} has no geometry. Skipping.")
                    continue
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
                    #print(
                    #    "Warning: Fixing feature {fid} in {stype} failed! No procedure defined to clean up geometry "
                    #    "type {geom_type}. Continuing anyway.".format(
                    #        fid=feature.GetFID(), stype=surface_type, geom_type=str(geom_type)
                    #    )
                    #)
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
                new_feature.SetField("relatieve_hoogteligging", feature["relatieveHoogteligging"])
                
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
    
    def identify_overlapping_surfaces(self):
        """Finds all overlapping surfaces and saves the surfaces with the highest relatieve hoogteligging"""
        layer = self.mem_database.GetLayerByName(SURFACES_TABLE_NAME)
        if layer is None:
            raise DatabaseOperationError
        
        # Check if the layer has any features
        if layer.GetFeatureCount() == 0:
            return
        
        # Create a list to store the features with the highest hoogteligging
        highest_surfaces = []
    
        # Loop through all surfaces in the layer
        for feature in layer:
            geom1 = feature.GetGeometryRef()  # Get the geometry of the current feature (surface)
            hoogteligging1 = feature.GetField("relatieve_hoogteligging")  # Get the "hoogteligging" field
            
            # Loop through all other surfaces in the layer to check for overlaps
            layer.ResetReading()  # Reset the reading to iterate over all features again
            for other_feature in layer:
                if other_feature.GetFID() == feature.GetFID():
                    # Skip comparing the surface with itself
                    continue
                
                geom2 = other_feature.GetGeometryRef()  # Get the geometry of the other feature
                if geom1.Intersects(geom2):  # Check if the geometries intersect (overlap)
                    hoogteligging2 = other_feature.GetField("relatieve_hoogteligging")  # Get the hoogteligging of the other feature
                    # Compare the two overlapping features and keep the one with the higher hoogteligging
                    if hoogteligging1 > hoogteligging2:
                        if feature not in highest_surfaces:
                            highest_surfaces.append(feature)  # Add the feature if it's not already in the list
                    elif hoogteligging1 < hoogteligging2:
                        if other_feature not in highest_surfaces:
                            highest_surfaces.append(other_feature)  # Add the other feature if it's not already in the list
    
        return highest_surfaces

    
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
        
        # List to track bui;ding-surfaces that are in the BGT but not in the BAG
        for surface in surfaces:
            if surface["surface_type"] == SURFACE_TYPE_PAND:
                if surface["identificatiebagpnd"] in building_dict.keys():
                    surface["build_year"] = building_dict[
                        surface["identificatiebagpnd"]
                    ]
                    surfaces.SetFeature(surface)
                else:
                    self.non_matching_buildings.append(surface)
            surface = None

        buildings = None
        surfaces = None
        print("... done")
        return
    
    def copy_features_with_matching_fields(self,src_layer, dst_layer, primary_key_field):
        # Get source layer definition
        src_defn = src_layer.GetLayerDefn()
        
        # Get the names of the fields in the destination layer
        dst_defn = dst_layer.GetLayerDefn()
        dst_field_names = [dst_defn.GetFieldDefn(i).GetName() for i in range(dst_defn.GetFieldCount())]
        
        # Iterate through the features in the source layer
        for src_feat in src_layer:
            # Create a new feature in the destination layer
            dst_feat = ogr.Feature(dst_defn)
            
            # Copy the fields from the source to the destination if the field names match
            for i in range(src_defn.GetFieldCount()):
                field_name = src_defn.GetFieldDefn(i).GetName()
                if field_name in dst_field_names:
                    dst_feat.SetField(field_name, src_feat.GetField(i))
            
            # Set the primary key manually if needed
            if primary_key_field:
                dst_feat.SetField(primary_key_field, src_feat.GetFID())
            
            # Set the geometry
            geom = src_feat.GetGeometryRef()
            if geom:
                dst_feat.SetGeometry(geom.Clone())
            
            # Add the feature to the destination layer
            dst_layer.CreateFeature(dst_feat)
            
            # Destroy the feature to free resources
            dst_feat = None
        
        # Sync the data to disk
        dst_layer.SyncToDisk()
    
    def _save_to_gpkg(self,file_folder,template_gpkg):
        print("Preparing template gpkg")
        file_name = self.set_output_name(file_folder)
        file_path = os.path.join(file_folder, file_name)
        self.copy_and_rename_file(template_gpkg, file_path)
        
        print("Saving layers to gpkg")
        # Initialize layers with common elements
        layers = [
            (CHECKS_TABLE_NAME, "2. Controles"),
            (PIPES_TABLE_NAME, "3. GWSW leidingen"),
            (RESULT_TABLE_NAME, "4. BGT inlooptabel"),
            (SURFACES_TABLE_NAME, "5. BGT oppervlakken"),
            (STATISTICS_TABLE_NAME, "6. Statistieken"),
            (SETTINGS_TABLE_NAME, "7. Rekeninstellingen")
        ]
        
        # Prepend the additional element if the layer exists
        if self.mem_database.GetLayerByName(INF_PAVEMENT_TABLE_NAME_PREV) is not None:
            layers.insert(0, (INF_PAVEMENT_TABLE_NAME_PREV, "1. Waterpasserende verharding en groene daken [optionele input]"))
        
        with self.open_gpkg(file_path) as dst_gpkg:
            for db_layer, gpkg_layer in layers:
                print(f"Saving {gpkg_layer} layer in gpkg")
                self._write_to_disk(dst_gpkg, db_layer, gpkg_layer)
                if db_layer == RESULT_TABLE_NAME:
                    self.track_changes(dst_gpkg)
           
        print("All layers saved successfully.")
    
    def set_output_name(self, file_folder):
        # Determine max. run_id
        max_run_id = -1
        for feature in self.settings_table: 
            run_id = feature.GetField("run_id")
            if run_id > max_run_id:
                max_run_id = run_id
    
        if max_run_id < 1:
            max_run_id = 1
        
        # Set the initial output name
        output_name = f"v{max_run_id}_BGT_inlooptabel.gpkg"
        file_path = os.path.join(file_folder, output_name)
        
        # Check if file already exists
        if os.path.exists(file_path):
            # Append current date and time to the output name
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"v{max_run_id}_BGT_inlooptabel_{current_time}.gpkg"
        
        return output_name 
    
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

            print(f"Template gpkg copied to {new_file_path}")
        except FileNotFoundError:
            print(f"The file {original_file_path} does not exist.")
        except PermissionError:
            print(f"Permission denied. Unable to copy {original_file_path} to {new_file_path}.")
        except Exception as e:
            print(f"An error occurred: {e}")
          
    
    def _write_to_disk(self, dst_gpkg, db_layer_name, dst_layer_name):
        """Copy self.mem_database to file_path"""
        # Get the source layer from the memory database
        db_layer = self.mem_database.GetLayerByName(db_layer_name)
        if db_layer is None:
            raise ValueError(f"Layer '{db_layer_name}' not found in memory database.")
        
        dst_layer = dst_gpkg.GetLayerByName(dst_layer_name)
        if dst_layer is None:
            raise ValueError(f"Layer '{dst_layer_name}' not found in destination GeoPackage.")
        
        layer_defn = db_layer.GetLayerDefn()
        dst_layer_defn = dst_layer.GetLayerDefn()
        
        if layer_defn.GetFieldCount() != dst_layer_defn.GetFieldCount():
            print(f"Warning: Source and destination layers have different field counts: {layer_defn.GetFieldCount()} vs {dst_layer_defn.GetFieldCount()}. Continuing anyway.")
        
        field_mapping = {dst_layer_defn.GetFieldDefn(i).GetName(): layer_defn.GetFieldIndex(dst_layer_defn.GetFieldDefn(i).GetName())
                 for i in range(dst_layer_defn.GetFieldCount())}

        # Iterate over features in the source layer and copy them to the destination layer
        for feature in db_layer:
            dst_feature = ogr.Feature(dst_layer_defn)
            for dst_field_name, src_field_index in field_mapping.items():
                if src_field_index != -1:  # Ensure the field exists in the source layer
                    dst_feature.SetField(dst_field_name, feature.GetField(src_field_index))
                else:
                    print(f"Warning: Source field '{dst_field_name}' not found in the source layer. Skipping field.")
            #for dst_field_name, src_field_index in field_mapping.items():
                #dst_feature.SetField(dst_field_name, feature.GetField(src_field_index))
            geom = feature.GetGeometryRef()
            if geom:
                dst_feature.SetGeometry(geom.Clone())
            dst_layer.CreateFeature(dst_feature)
            dst_feature = None
        print(f"Layer '{dst_layer_name}' saved successfully.")

    @contextlib.contextmanager
    def open_gpkg(self, file_path):
        dst_gpkg = GPKG_DRIVER.Open(file_path, 1)
        if dst_gpkg is None:
            raise ValueError(f"Could not open GeoPackage '{file_path}' for writing.")
        try:
            yield dst_gpkg
        finally:
            dst_gpkg = None

    def track_changes(self, dst_gpkg):
        """ Add SQL triggers to track changes """
        
        # SQL statements to create the triggers
        sql_time_last_change = """
        CREATE TRIGGER update_laaste_wijziging_on_update AFTER UPDATE
        OF bgt_identificatie, type_verharding, graad_verharding, hellingstype, hellingspercentage, type_private_voorziening, berging_private_voorziening, leidingcode_gemengd, leidingcode_hwa, leidingcode_dwa, leidingcode_infiltratie, gemengd_riool, hemelwaterriool, vgs_hemelwaterriool, vuilwaterriool, infiltratievoorziening, open_water, maaiveld
        ON "4. BGT inlooptabel"
        FOR EACH ROW
        BEGIN
        UPDATE "4. BGT inlooptabel" SET laatste_wijziging = CURRENT_TIMESTAMP WHERE id = old.id;
        END 
        """
        
        sql_changed_tf = """
        CREATE TRIGGER update_wijziging_on_update AFTER UPDATE
        OF bgt_identificatie, type_verharding, graad_verharding, hellingstype, hellingspercentage, type_private_voorziening, berging_private_voorziening, leidingcode_gemengd, leidingcode_hwa, leidingcode_dwa, leidingcode_infiltratie, gemengd_riool, hemelwaterriool, vgs_hemelwaterriool, vuilwaterriool, infiltratievoorziening, open_water, maaiveld
        ON "4. BGT inlooptabel"
        FOR EACH ROW
        BEGIN
        UPDATE "4. BGT inlooptabel" SET wijziging = 1 WHERE id = old.id;
        END
        """
        
        # Execute the SQL statements
        dst_gpkg.ExecuteSQL(sql_time_last_change)
        dst_gpkg.ExecuteSQL(sql_changed_tf)

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
