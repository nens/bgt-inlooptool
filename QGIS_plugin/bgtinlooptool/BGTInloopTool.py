# -*- coding: utf-8 -*-
"""
/***************************************************************************
 BGTInloopTool
                                 A QGIS plugin
 BGT Inlooptool
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-08-12
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Leendert van Wolfswinkel, Emile de Badts
        email                : emile.debadts@nelen-schuurmans.nl
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os.path
import sys
import json


from PyQt5.QtCore import QUrl, QByteArray
from PyQt5.QtNetwork import QNetworkRequest
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

# Initialize Qt resources from file resources.py
from .resources import *

# Import the code for the dialog
from .BGTInloopTool_dialog import BGTInloopToolDialog

# Import the BGT Inlooptool core
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from core.inlooptool import *
from core.constants import *
from .ogr2qgis import *

MESSAGE_CATEGORY = "BGT Inlooptool"
BGT_API_URL = "https://api.pdok.nl/lv/bgt/download/v1_0/full/custom"

INLOOPTABEL_STYLE = os.path.join(
    os.path.dirname(__file__), "style", "bgt_inlooptabel.qml"
)
PIPES_STYLE = os.path.join(os.path.dirname(__file__), "style", "gwsw_lijn.qml")
BGT_STYLE = os.path.join(os.path.dirname(__file__), "style", "bgt_oppervlakken.qml")


class InloopToolTask(QgsTask):
    def __init__(
        self,
        description,
        parameters,
        bgt_file,
        pipe_file,
        building_file,
        kolken_file,
        input_extent_mask_wkt,
    ):
        super().__init__(description, QgsTask.CanCancel)

        iface.messageBar().pushMessage(
            MESSAGE_CATEGORY,
            "Afwateringskenmerken BGT vlakken bepalen...",
            level=Qgis.Info,
        )
        iface.mainWindow().repaint()  # to show the message before the task starts

        self.parameters = parameters
        self.bgt_file = bgt_file
        self.pipe_file = pipe_file
        self.building_file = building_file
        self.kolken_file = kolken_file
        self.input_extent_mask_wkt = input_extent_mask_wkt
        self.exception = None
        self.setProgress(0)
        self.total_progress = 5
        if self.parameters.gebruik_kolken:
            self.total_progress += 1
        if self.parameters.gebruik_bag:
            self.total_progress += 1
        if self.input_extent_mask_wkt is not None:
            self.total_progress += 1

    def increase_progress(self):
        self.setProgress(self.progress() + 100 / self.total_progress)

    def run(self):
        try:
            QgsMessageLog.logMessage(
                "Started inlooptool task", MESSAGE_CATEGORY, level=Qgis.Info
            )
            self.it = InloopTool(self.parameters)
            self.increase_progress()

            QgsMessageLog.logMessage(
                "Importing surfaces", MESSAGE_CATEGORY, level=Qgis.Info
            )
            self.it.import_surfaces(self.bgt_file)
            self.increase_progress()

            QgsMessageLog.logMessage(
                "Importing pipes", MESSAGE_CATEGORY, level=Qgis.Info
            )
            self.it.import_pipes(self.pipe_file)
            self.increase_progress()

            if self.parameters.gebruik_kolken:
                QgsMessageLog.logMessage(
                    "Importing kolken", MESSAGE_CATEGORY, level=Qgis.Info
                )
                self.it.import_kolken(self.kolken_file)
                self.increase_progress()

            # Note: buildings are not imported to database.
            # self.it._database.add_build_year_to_surface() just reads the build year without copying the layer

            QgsMessageLog.logMessage(
                " -- Adding index to inputs...", MESSAGE_CATEGORY, level=Qgis.Info
            )
            self.it._database.add_index_to_inputs(kolken=self.parameters.gebruik_kolken)
            QgsMessageLog.logMessage(
                " -- Finished adding index to inputs", MESSAGE_CATEGORY, level=Qgis.Info
            )

            if self.parameters.gebruik_bag:
                QgsMessageLog.logMessage(
                    "Adding build year to surfaces", MESSAGE_CATEGORY, level=Qgis.Info
                )
                self.it._database.add_build_year_to_surface(
                    file_path=self.building_file
                )
                self.increase_progress()

            if self.input_extent_mask_wkt is not None:
                QgsMessageLog.logMessage(
                    "Clipping inputs to extent", MESSAGE_CATEGORY, level=Qgis.Info
                )
                self.it._database.remove_input_features_outside_clip_extent(
                    self.input_extent_mask_wkt
                )
                self.increase_progress()
                QgsMessageLog.logMessage(
                    "Adding index to inputs...", MESSAGE_CATEGORY, level=Qgis.Info
                )
                self.it._database.add_index_to_inputs(
                    kolken=self.parameters.gebruik_kolken
                )

            QgsMessageLog.logMessage(
                "Calculating distances", MESSAGE_CATEGORY, level=Qgis.Info
            )
            self.it.calculate_distances(parameters=self.parameters)
            self.increase_progress()

            QgsMessageLog.logMessage(
                "Calculating runoff targets", MESSAGE_CATEGORY, level=Qgis.Info
            )
            self.it.calculate_runoff_targets()
            self.increase_progress()

            QgsMessageLog.logMessage("Finished", MESSAGE_CATEGORY, level=Qgis.Success)
            return True
        except Exception as e:
            self.exception = e
            return False

    def finished(self, result):

        if result:
            root = QgsProject.instance().layerTreeRoot()
            layer_group = root.insertGroup(0, MESSAGE_CATEGORY)

            self.add_to_layer_group(
                db_layer_name=SURFACES_TABLE_NAME,
                layer_tree_layer_name="BGT Oppervlakken",
                qml=BGT_STYLE,
                layer_group=layer_group,
            )
            self.add_to_layer_group(
                db_layer_name=RESULT_TABLE_NAME,
                layer_tree_layer_name="BGT Inlooptabel",
                qml=INLOOPTABEL_STYLE,
                layer_group=layer_group,
            )
            self.add_to_layer_group(
                db_layer_name=PIPES_TABLE_NAME,
                layer_tree_layer_name="GWSW Leidingen",
                qml=PIPES_STYLE,
                layer_group=layer_group,
            )
            iface.messageBar().pushMessage(
                MESSAGE_CATEGORY,
                "Afwateringskenmerken BGT bepaald!",
                level=Qgis.Success,
            )

        else:
            if self.exception is None:
                iface.messageBar().pushMessage(
                    MESSAGE_CATEGORY,
                    "Bepalen afwateringskenmerken BGT mislukt",
                    level=Qgis.Critical,
                )
            else:
                print(str(self.exception))
                message = "Bepalen afwateringskenmerken BGT mislukt"
                if isinstance(self.exception, FileInputError):
                    message += ": " + str(self.exception)
                iface.messageBar().clearWidgets()
                iface.messageBar().pushMessage(
                    MESSAGE_CATEGORY, message, level=Qgis.Critical
                )
                # raise self.exception

    def cancel(self):
        iface.messageBar().pushMessage(
            MESSAGE_CATEGORY,
            "Bepalen afwateringskenmerken BGT afgebroken door de foutmelding: {}",
            level=Qgis.Critical,
        )
        super().cancel()

    def add_to_layer_group(
        self, db_layer_name: str, layer_tree_layer_name: str, qml: str, layer_group
    ):
        ogr_lyr = self.it._database.mem_database.GetLayerByName(db_layer_name)
        if ogr_lyr is not None:
            if ogr_lyr.GetFeatureCount() > 0:
                qgs_lyr = as_qgis_memory_layer(ogr_lyr, layer_tree_layer_name)
                project = QgsProject.instance()
                project.addMapLayer(qgs_lyr, addToLegend=False)
                layer_group.insertLayer(0, qgs_lyr)
                qgs_lyr.loadNamedStyle(qml)
                qgs_lyr.triggerRepaint()


class BGTInloopTool:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """

        # Save reference to the QGIS interface
        self.iface = iface
        self.tm = QgsApplication.taskManager()

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # Declare instance attributes
        self.actions = []
        self.menu = "&BGT Inlooptool"

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None,
    ):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ":/plugins/BGTInloopTool/icon.png"
        self.add_action(
            icon_path,
            text="BGT Inlooptool",
            callback=self.run,
            parent=self.iface.mainWindow(),
        )

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu("&BGT Inlooptool", action)
            self.iface.removeToolBarIcon(action)

    def validate_extent_layer(self, extent_layer):

        # Check feature count in the selected layer
        extent_feature_count = extent_layer.featureCount()
        QgsMessageLog.logMessage(
            f"Found {extent_feature_count} features in extent layer",
            MESSAGE_CATEGORY,
            level=Qgis.Info,
        )

        selected_feature_count = extent_layer.selectedFeatureCount()
        QgsMessageLog.logMessage(
            f"Found {selected_feature_count} selected features in extent layer",
            MESSAGE_CATEGORY,
            level=Qgis.Info,
        )

        extent_layer_crs = extent_layer.crs()
        if extent_layer_crs != "EPSG:28992":
            reproject = True

        if extent_feature_count == 1:
            # to get the first and only feature you think you might do extent_layer.getFeature(1),
            # but this does not work for shapefiles. Why? WHY?
            for feat in extent_layer.getFeatures():
                extent_feature = feat
            extent_geometry = extent_feature.geometry()
        elif selected_feature_count == 1:
            selected_feature = extent_layer.selectedFeatures()[0]
            extent_geometry = selected_feature.geometry()
        elif extent_feature_count > 1:
            self.iface.messageBar().pushMessage(
                MESSAGE_CATEGORY,
                "Laag voor gebiedsselectie bevat meer dan één polygoon / feature. "
                "Selecteer er maximaal één en probeer opnieuw.",
                level=Qgis.Warning,
                duration=10,
            )
            return False
        elif extent_feature_count == 0:
            self.iface.messageBar().pushMessage(
                MESSAGE_CATEGORY,
                "Laag voor gebiedsselectie bevat geen features",
                level=Qgis.Warning,
            )
            return False
        else:
            self.iface.messageBar().pushMessage(
                MESSAGE_CATEGORY,
                "Laag voor gebiedsselectie is niet geschikt",
                level=Qgis.Warning,
            )
            return False

        if extent_geometry.isNull():
            self.iface.messageBar().pushMessage(
                MESSAGE_CATEGORY,
                "Geselecteerde laag of feature heeft geen geometrie. "
                "Sla wijzigingen aan de laag eerst op en probeer opnieuw",
                level=Qgis.Warning,
            )
            return False

        if reproject:
            out_crs = QgsCoordinateReferenceSystem("EPSG:28992")
            transform = QgsCoordinateTransform(
                extent_layer_crs, out_crs, QgsProject.instance()
            )
            extent_geometry.transform(transform)
            extent_geometry_wkt = extent_geometry.asWkt()
        else:
            extent_geometry_wkt = extent_geometry.asWkt()

        return extent_geometry_wkt

    def download_bgt_from_api(self):

        extent_layer = self.dlg.BGTExtentCombobox.currentLayer()
        output_zip = self.dlg.bgtApiOutput.filePath()

        extent_geometry_wkt = self.validate_extent_layer(extent_layer)
        if not extent_geometry_wkt:
            return

        self.iface.messageBar().pushMessage(
            MESSAGE_CATEGORY,
            f"Begonnen met downloaden van BGT lagen naar {output_zip}",
            level=Qgis.Info,
            duration=5,
        )
        self.iface.mainWindow().repaint()  # to show the message before the task starts

        # Use the extent geometry to extract surfaces for the given extent
        nam = QgsBlockingNetworkRequest()

        networkrequest = QNetworkRequest(QUrl.fromUserInput(BGT_API_URL))
        networkrequest.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")

        data = {
            "featuretypes": list(ALL_USED_SURFACE_TYPES),
            "format": "gmllight",
            "geofilter": extent_geometry_wkt,
        }

        data_array = QByteArray()
        data_array.append(json.dumps(data))

        response = nam.post(networkrequest, data_array)

        response_bytes = bytes(nam.reply().content())
        response_json = json.loads(response_bytes.decode("ascii"))

        download_id = response_json["downloadRequestId"]
        status_link = BGT_API_URL + "/" + download_id + "/status"

        status = "PENDING"
        while status != "COMPLETED":
            status_request = QNetworkRequest(QUrl.fromUserInput(status_link))
            status_response = nam.get(status_request)
            status_response_bytes = bytes(nam.reply().content())
            status_response_json = json.loads(status_response_bytes.decode("ascii"))
            status = status_response_json["status"]
            time.sleep(5)

        download_url_extract = status_response_json["_links"]["download"]["href"]
        download_url = "https://api.pdok.nl" + download_url_extract

        download_request = QNetworkRequest(QUrl.fromUserInput(download_url))
        download_response = nam.get(download_request)
        with open(output_zip, "wb") as f:
            f.write(nam.reply().content())
        self.iface.messageBar().pushMessage(
            MESSAGE_CATEGORY,
            f'BGT lagen gedownload naar <a href="{output_zip}">{output_zip}</a>',
            level=Qgis.Info,
            duration=20,  # wat langer zodat gebruiker tijd heeft om op linkje te klikken
        )
        self.dlg.bgt_file.setFilePath(output_zip)
        self.dlg.inputExtentComboBox.setLayer(extent_layer)
        self.dlg.inputExtentComboBox.setEnabled(True)
        self.dlg.inputExtentGroupBox.setChecked(True)

    def on_run(self):

        # input files
        bgt_file = self.dlg.bgt_file.filePath()
        pipe_file = self.dlg.pipe_file.filePath()
        building_file = self.dlg.building_file.filePath()
        kolken_file = self.dlg.kolken_file.filePath()

        if self.dlg.inputExtentGroupBox.isChecked():
            extent_layer = self.dlg.inputExtentComboBox.currentLayer()
            extent_geometry_wkt = self.validate_extent_layer(extent_layer)
            if not extent_geometry_wkt:
                return
        else:
            extent_geometry_wkt = None

        # Iniate bgt inlooptool class with parameters
        parameters = InputParameters(
            max_afstand_vlak_afwateringsvoorziening=self.dlg.max_afstand_vlak_afwateringsvoorziening.value(),
            max_afstand_vlak_oppwater=self.dlg.max_afstand_vlak_oppwater.value(),
            max_afstand_pand_oppwater=self.dlg.max_afstand_pand_oppwater.value(),
            max_afstand_vlak_kolk=self.dlg.max_afstand_vlak_kolk.value(),
            max_afstand_afgekoppeld=self.dlg.max_afstand_afgekoppeld.value(),
            max_afstand_drievoudig=self.dlg.max_afstand_drievoudig.value(),
            afkoppelen_hellende_daken=self.dlg.afkoppelen_hellende_daken.isChecked(),
            gebruik_bag=building_file != "",
            gebruik_kolken=kolken_file != "",
            bouwjaar_gescheiden_binnenhuisriolering=self.dlg.bouwjaar_gescheiden_binnenhuisriolering.value(),
            verhardingsgraad_erf=self.dlg.verhardingsgraad_erf.value(),
            verhardingsgraad_half_verhard=self.dlg.verhardingsgraad_half_verhard.value(),
        )

        inlooptooltask = InloopToolTask(
            description="Inlooptool task",
            parameters=parameters,
            bgt_file=bgt_file,
            pipe_file=pipe_file,
            building_file=building_file,
            kolken_file=kolken_file,
            input_extent_mask_wkt=extent_geometry_wkt,
        )

        self.tm.addTask(inlooptooltask)

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start is True:
            self.first_start = False

            self.dlg = BGTInloopToolDialog()

            # Initiating the tool in 'on_run'
            self.dlg.pushButtonRun.clicked.connect(self.on_run)
            self.dlg.pushButtonDownloadBGT.clicked.connect(self.download_bgt_from_api)

        # Create a mask layer for clipping and extracting bgt surfaces
        # mask_polygon = QgsVectorLayer("Polygon?crs=epsg:28992", "Extent layer", "memory")
        # project = QgsProject.instance()
        # project.addMapLayer(mask_polygon)

        # show the dialog
        self.dlg.show()