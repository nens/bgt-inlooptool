# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 08:42:41 2023

@author: ruben.vanderzaag
"""
from core.table_schemas import *
from core.constants import *
from core.defaults import *

from osgeo import ogr
import pandas as pd

# Path to the Geopackage file
gpkg_path = 'bgt_zeewolde3.gpkg'

# Open the Geopackage
gpkg_ds_BGT = ogr.Open(gpkg_path, 0)  # 0 means read-only mode

# Check if the Geopackage was successfully opened
if gpkg_ds_BGT is None:
    print("Failed to open the Geopackage.")
else:
    print("Successfully opened the Geopackage.")
    layername = {}
    # Iterate over all layers in the Geopackage and print their names
    for i in range(gpkg_ds_BGT.GetLayerCount()):
        locals()["BGT_layer_"+str(i)] = gpkg_ds_BGT.GetLayerByIndex(i)
        layer = locals()["BGT_layer_"+str(i)]
        #layer = gpkg_ds.GetLayerByIndex(i)
        print(f"Layer {i}: {layer.GetName()}")


result = {
    TARGET_TYPE_GEMENGD_RIOOL: 0,
    TARGET_TYPE_HEMELWATERRIOOL: 0,
    TARGET_TYPE_VGS_HEMELWATERRIOOL: 0,
    TARGET_TYPE_VUILWATERRIOOL: 0,
    TARGET_TYPE_INFILTRATIEVOORZIENING: 0,
    TARGET_TYPE_OPEN_WATER: 0,
    TARGET_TYPE_MAAIVELD: 0,
}
surfaces = BGT_layer_22

data = []
for feature in surfaces:
    attributes = feature.items()
    data.append(attributes)

# Create a DataFrame from the attribute data
df = pd.DataFrame(data)

for surface in df:
    print('succes')
    #print(surface["plus-status"])
    
for surface in surfaces:
    print(surface["plus-status"])



for index, surface in df.iterrows():
    print(f"Index: {index}")

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
        return False
    else:
        if surface.build_year is None:
            return False
        else:
            return (
                surface.build_year
                > parameters.bouwjaar_gescheiden_binnenhuisriolering
            )

def hellend_dak():
    return True


for distance_type in DISTANCE_TYPES:
    field_name = "distance_" + distance_type
    field_type = ogr.OFTReal
    field_width = 50
    new_field_defn = ogr.FieldDefn(field_name,field_type)
    new_field_defn.SetWidth(field_width)
    surfaces.CreateField(new_field_defn)
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