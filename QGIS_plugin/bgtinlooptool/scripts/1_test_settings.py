# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 12:38:03 2024

@author: ruben.vanderzaag
"""

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


#Step 2: fill database with data (test with pipes)
parameters = InputParameters()
it = InloopTool(parameters)
pipe_file = r"C:\Users\ruben.vanderzaag\Documents\Github\bgt-inlooptool\QGIS_plugin\bgtinlooptool\style\test_input\Amersfoort_GWSW.gpkg"
it.import_pipes(pipe_file)

#Step 3: write pipes to empty output gpkg
_database = Database_v2()
it._database.add_index_to_inputs()
GPKG_DRIVER = ogr.GetDriverByName("GPKG")

#Step 4: creating a new settings table in the same db
        self.create_table(
            table_name=SETTINGS_TABLE_NAME, table_schema=SETTINGS_TABLE_SCHEMA
        )
        
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