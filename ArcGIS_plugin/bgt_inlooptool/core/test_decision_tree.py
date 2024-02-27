# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 11:44:08 2023

@author: ruben.vanderzaag
"""

from osgeo import ogr
# Local imports
from core.table_schemas import *
from core.constants import *
from core.defaults import *

# Specify the GeoPackage file and layer name
geopackage_file = r"G:\Projecten Y (2023)\Y0127 - BGT Inlooptabel Nieuwe Versie 2024\Gegevens\Bewerking\testdata\surfaces_result_akersloot.gpkg"
layer_name = "bgt_oppervlakken"

# Open the GeoPackage file
driver = ogr.GetDriverByName("GPKG")
geopackage_ds = ogr.Open(geopackage_file, 0)  # 0 means read-only mode

if geopackage_ds is None:
    print("Failed to open GeoPackage.")
    exit(1)

# Access the specified layer within the GeoPackage
layer = geopackage_ds.GetLayerByName(layer_name)

if layer is None:
    print(f"Layer '{layer_name}' not found in the GeoPackage.")
    geopackage_ds = None  # Close the GeoPackage dataset
    exit(1)

# Now you can work with the layer using the 'layer' variable
# For example, you can iterate over features in the layer:
for feature in layer:
    # Process each feature as needed
    if feature["identificatie_lokaalid"]=="G0383.845e720715aa4a5dbd46cf2e41b285ae":
        print("Fid = ",feature.GetFID(), "pand_id = ",feature["identificatie_lokaalid"])
        surface = feature

for feature in layer:
    # Process each feature as needed
    if feature["identificatie_lokaalid"]=="G0383.cb7228cdf4594007ae95811d12d49770":
        print("Fid = ",feature.GetFID(), "pand_id = ",feature["identificatie_lokaalid"])
        surface = feature


surface = layer
result = {
    TARGET_TYPE_GEMENGD_RIOOL: 0,
    TARGET_TYPE_HEMELWATERRIOOL: 0,
    TARGET_TYPE_VGS_HEMELWATERRIOOL: 0,
    TARGET_TYPE_VUILWATERRIOOL: 0,
    TARGET_TYPE_INFILTRATIEVOORZIENING: 0,
    TARGET_TYPE_OPEN_WATER: 0,
    TARGET_TYPE_MAAIVELD: 0,
}

import pandas as pd
# Extract data from the layer (geometry and attributes)
data = []
feature = surface
geometry = feature.GetGeometryRef()
attributes = feature.items()
data.append({'geometry': geometry.ExportToWkt(), **attributes})

# Create a DataFrame
df = pd.DataFrame(data)

parameters = {
    "max_afstand_vlak_afwateringsvoorziening": 40,
    "max_afstand_vlak_oppwater": 2,
    "max_afstand_pand_oppwater": 6,
    "max_afstand_vlak_kolk": 30,
    "max_afstand_afgekoppeld": 4,
    "max_afstand_drievoudig": 4,
    "afkoppelen_hellende_daken": True,
    "gebruik_bag": False,
    "gebruik_kolken": False,
    "bouwjaar_gescheiden_binnenhuisriolering": 2017,
    "verhardingsgraad_erf": 50,
    "verhardingsgraad_half_verhard": 50
    }


text = """
MAX_AFSTAND_VLAK_AFWATERINGSVOORZIENING: 40,
MAX_AFSTAND_VLAK_OPPWATER: 2,
MAX_AFSTAND_PAND_OPPWATER: 6,
MAX_AFSTAND_VLAK_KOLK: 30,
MAX_AFSTAND_AFGEKOPPELD: 3,
MAX_AFSTAND_DRIEVOUDIG: 4,
AFKOPPELEN_HELLENDE_DAKEN: True,
GEBRUIK_BAG: False,
GEBRUIK_KOLKEN: False,
BOUWJAAR_GESCHEIDEN_BINNENHUISRIOLERING: 1992,
VERHARDINGSGRAAD_ERF: 50,
VERHARDINGSGRAAD_HALF_VERHARD: 50
"""

# Replace capital letters with lowercase
text_lowercase = text.lower()

print(text_lowercase)
#decision tree:

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
        surface["distance_" + OPEN_WATER] < parameters["max_afstand_vlak_oppwater"]
    )

def bij_kolk():
    if parameters.gebruik_kolken:
        return surface["distance_" + KOLK] < parametersp["max_afstand_vlak_kolk"]
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
            <= parameters["max_afstand_afgekoppeld"]
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
    if surface.build_year is None:
        return False
    else:
        return (
            surface.build_year
            > parameters["bouwjaar_gescheiden_binnenhuisriolering"]
        )

def hellend_dak():
    return True

for distance_type in DISTANCE_TYPES:
    if surface["distance_" + distance_type] is None:
        surface["distance_" + distance_type] = PSEUDO_INFINITE
        #print(surface["distance_" + distance_type])

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
        
        if parameters["afkoppelen_hellende_daken"]:

            if nieuw_pand() and hellend_dak():

                if hwa_dichterbij_dan_hwavgs_en_infiltr():
                    result[TARGET_TYPE_HEMELWATERRIOOL] = 100
                    print("joejoeee")
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
                        print("joee")
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