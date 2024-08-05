# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 14:39:22 2024

@author: ruben.vanderzaag
"""

import os.path
import sys
import json
os.chdir(r"C:\Users\ruben.vanderzaag\Documents\Github\bgt-inlooptool\QGIS_plugin\bgtinlooptool")

from PyQt5.QtCore import QUrl, QByteArray
from PyQt5.QtNetwork import QNetworkRequest
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import (
    QgsProject,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsBlockingNetworkRequest,
)
from qgis.core import (
    QgsTask,
    Qgis,
    QgsApplication,
    QgsMessageLog,
)
from qgis.utils import iface
"""
# Initialize Qt resources from file resources.py
from resources import *

# Import the code for the dialog
#from BGTInloopTool_dialog import BGTInloopToolDialog

# Import the BGT Inlooptool core
#sys.path.append(os.path.dirname(os.path.realpath(__file__)))
os.chdir(r"C:\Users\ruben.vanderzaag\Documents\Github\bgt-inlooptool")
from core.inlooptool import *
from core.constants import *
os.chdir(r"C:\Users\ruben.vanderzaag\Documents\Github\bgt-inlooptool\QGIS_plugin\bgtinlooptool")
#from ogr2qgis import *

MESSAGE_CATEGORY = "BGT Inlooptool"
BGT_API_URL = "https://api.pdok.nl/lv/bgt/download/v1_0/full/custom"
"""
INLOOPTABEL_STYLE = os.path.join(
    os.path.dirname(__file__), "style", "bgt_inlooptabel.qml"
)
PIPES_STYLE = os.path.join(os.path.dirname(__file__), "style", "gwsw_lijn.qml")
BGT_STYLE = os.path.join(os.path.dirname(__file__), "style", "bgt_oppervlakken.qml")

TEMPLATE_GPKG = os.path.join(os.path.dirname(__file__), "style", "template_output.gkpg")
"""
TEMPLATE_GPKG = os.path.join(os.getcwd(),"style", "template_output.gpkg")
OUTPUT_GPKG = os.path.join(os.getcwd(),"style", "output_bgtinlooptool.gpkg")

#Step 1: make copy from output template
import os

def copy_and_rename_file(original_file_path, new_file_path):
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

copy_and_rename_file(TEMPLATE_GPKG, OUTPUT_GPKG)

#Step 2: fill database with data (test with pipes)
parameters = InputParameters()
it = InloopTool(parameters)
pipe_file = r"C:\Users\ruben.vanderzaag\Documents\Github\bgt-inlooptool\QGIS_plugin\bgtinlooptool\style\test_input\Amersfoort_GWSW.gpkg"
it.import_pipes(pipe_file)

#Step 3: write pipes to empty output gpkg
_database = Database_v2()
it._database.add_index_to_inputs()
GPKG_DRIVER = ogr.GetDriverByName("GPKG")

#Onderstaande deel werkt: kopieert data van 1 gpkg laag naar een andere. 

from osgeo import ogr, osr

# Function to append features from source layer to target layer
def append_features_to_layer(src_gpkg_path, src_layer_name, dst_gpkg_path, dst_layer_name):
    # Open the source GeoPackage
    src_driver = ogr.GetDriverByName("GPKG")
    src_gpkg = src_driver.Open(src_gpkg_path, 0)  # 0 means read-only

    if not src_gpkg:
        raise Exception("Failed to open source GeoPackage")

    # Open the target GeoPackage
    dst_driver = ogr.GetDriverByName("GPKG")
    dst_gpkg = dst_driver.Open(dst_gpkg_path, 1)  # 1 means writable

    if not dst_gpkg:
        raise Exception("Failed to open destination GeoPackage")

    # Get the source and target layers
    src_layer = src_gpkg.GetLayerByName(src_layer_name)
    dst_layer = dst_gpkg.GetLayerByName(dst_layer_name)

    if not src_layer:
        raise Exception(f"Source layer {src_layer_name} not found in the GeoPackage")

    if not dst_layer:
        raise Exception(f"Destination layer {dst_layer_name} not found in the GeoPackage")

    # Check if the source and target layers have the same spatial reference
    src_srs = src_layer.GetSpatialRef()
    dst_srs = dst_layer.GetSpatialRef()

    if not src_srs.IsSame(dst_srs):
        raise Exception("Spatial references do not match")

    # Append features from the source layer to the target layer
    for feature in src_layer:
        dst_layer.CreateFeature(feature.Clone())

    # Cleanup
    src_gpkg = None
    dst_gpkg = None

    print("Features appended to target layer successfully")

# Example usage
src_gpkg_path = r"C:\Users\ruben.vanderzaag\Documents\Github\bgt-inlooptool\QGIS_plugin\bgtinlooptool\style\test_input\Amersfoort_GWSW.gpkg"
src_layer_name = "default_lijn"
dst_gpkg_path = r"C:\Users\ruben.vanderzaag\Documents\Github\bgt-inlooptool\QGIS_plugin\bgtinlooptool\style\Amersfoort_empty.gpkg"
dst_layer_name = "default_lijn"

append_features_to_layer(src_gpkg_path, src_layer_name, dst_gpkg_path, dst_layer_name)


#READ TEST DATA as OGR layer
# Path to your GeoPackage file
gpkg_file = r"C:\Users\ruben.vanderzaag\Documents\Github\bgt-inlooptool\QGIS_plugin\bgtinlooptool\style\output_bgtinlooptool_v4.gpkg"
# Open the GeoPackage file
data_source = ogr.Open(gpkg_file, 0)  # 0 means read-only, 1 means read-write
# Get the layer by name (replace 'your_layer_name' with the actual layer name)
layer_name = 'pipes'
layer = data_source.GetLayerByName(layer_name)
dst_gpkg_path = r"C:\Users\ruben.vanderzaag\Documents\Github\bgt-inlooptool\QGIS_plugin\bgtinlooptool\style\test_pipes.gpkg"
dst_layer_name = "pipes"

dst_driver = ogr.GetDriverByName("GPKG")
dst_gpkg = dst_driver.Open(dst_gpkg_path, 1)  # 1 means writable
dst_layer = dst_gpkg.GetLayerByName(dst_layer_name)

# Get the layer definition to access field information
layer_defn = layer.GetLayerDefn()

# Check if field definitions match; if not, create fields in the destination layer
dst_layer_defn = dst_layer.GetLayerDefn()
for i in range(layer_defn.GetFieldCount()):
    src_field_defn = layer_defn.GetFieldDefn(i)
    dst_field_defn = dst_layer_defn.GetFieldDefn(i) if i < dst_layer_defn.GetFieldCount() else None
    
    if not dst_field_defn or src_field_defn.GetName() != dst_field_defn.GetName():
        print(f"{src_field_defn.GetName()} {dst_field_defn.GetName()}")
        #dst_layer.CreateField(src_field_defn)

for feature in layer:
    # Print feature ID
    print(f"Feature ID: {feature.GetFID()}")
    
    # Print each field's name and value
    for i in range(layer_defn.GetFieldCount()):
        field_name = layer_defn.GetFieldDefn(i).GetName()
        print(field_name)
        field_value = feature.GetField(i)
        print(f"{field_name}: {field_value}")
    
    dst_layer.CreateFeature(feature.Clone())

dst_gpkg = None
dst_layer = None
feature = None
layer = None


#Correctie template gpkg (remove fid field)
import sqlite3
import os

def remove_field_from_gpkg_layer(gpkg_path: str, layer_name: str, field_name: str):
    if not os.path.exists(gpkg_path):
        print(f"GeoPackage '{gpkg_path}' not found.")
        return
    
    conn = sqlite3.connect(gpkg_path)
    cursor = conn.cursor()
    
    # Check if the table (layer) exists
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (layer_name,))
    if not cursor.fetchone():
        print(f"Layer '{layer_name}' not found in GeoPackage '{gpkg_path}'.")
        conn.close()
        return
    
    # Check if the field (column) exists
    cursor.execute(f"PRAGMA table_info({layer_name})")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    
    if field_name not in column_names:
        print(f"Field '{field_name}' not found in layer '{layer_name}'.")
        conn.close()
        return
    
    # Create a new table without the specified column
    column_names.remove(field_name)
    new_columns = ", ".join([f'"{col}"' for col in column_names])
    
    cursor.execute(f'ALTER TABLE "{layer_name}" RENAME TO "{layer_name}_old"')
    cursor.execute(f'CREATE TABLE "{layer_name}" AS SELECT {new_columns} FROM "{layer_name}_old"')
    
    # Copy indexes, triggers, and constraints from the old table to the new table
    cursor.execute(f"PRAGMA foreign_key_list('{layer_name}_old')")
    foreign_keys = cursor.fetchall()
    for key in foreign_keys:
        cursor.execute(f'ALTER TABLE "{layer_name}" ADD CONSTRAINT "{key[2]}" FOREIGN KEY("{key[3]}") REFERENCES "{key[4]}"("{key[5]}")')
    
    # Drop the old table
    cursor.execute(f'DROP TABLE "{layer_name}_old"')
    
    conn.commit()
    conn.close()
    
    print(f"Field '{field_name}' removed from layer '{layer_name}'.")

# Example usage
gpkg_path = r"C:\Users\ruben.vanderzaag\Documents\Github\bgt-inlooptool\QGIS_plugin\bgtinlooptool\style\template_output.gpkg"

remove_field_from_gpkg_layer(gpkg_path, "1. Waterpasserende verharding [optionele input]", "fid")
remove_field_from_gpkg_layer(gpkg_path, "3. GWSW leidingen", "fid")
remove_field_from_gpkg_layer(gpkg_path, "4. BGT inlooptabel", "fid")
remove_field_from_gpkg_layer(gpkg_path, "5. BGT oppervlakken", "fid")

#Step 4: de 3 basislagen verzamelen en opslaan in deze gpkg

    #Zie functie _save_to_gpkg in core

#Step 5: handmatige wijziging kolom toevoegen aan BGT inlooptabel

#Step 6: laag rekeninstellingen aanmaken en opslaan in gpkg
#Ook output path wegschrijven, zodat hier revisieoverzicht bijgehouden kan worden.

#Step 7: laag controles aanmaken en opslaan

#Step 8: laag statistieken aanmaken en opslaan

