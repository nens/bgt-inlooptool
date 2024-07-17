# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessing,
    QgsProcessingParameterFile,
    QgsProject
)

from bgtinlooptool.core.inlooptool import InputParameters
from bgtinlooptool.core.inlooptool import InloopTool
from bgtinlooptool.ogr2qgis import as_qgis_memory_layer
from bgtinlooptool.constants import BGT_STYLE


class BGTDownload2QgisAlgorithm(QgsProcessingAlgorithm):
    """
    Converts a download zip archive of BGT .gml files to a BGT surfaces layer
    """
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'

    def createInstance(self):
        return BGTDownload2QgisAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'bgt_download2qgis'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return 'BGT zip file naar BGT oppervlakkenlaag'

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return 'BGT Oppervlakken'

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'bgt_inlooptool'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return ("Converteert een zip archief met BGT lagen in .gml formaat naar een QGIS vectorlaag zoals gebruikt door "
                "de BGT Inlooptool")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        # We add the input vector features source. It can have any kind of
        # geometry.
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT,
                "Gedownloade BGT ZIP"
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        source = self.parameterAsFile(
            parameters,
            self.INPUT,
            context
        )

        # Create a dictionary to hold the unique values from the
        # dissolve_field and the sum of the values from the sum_field

        inlooptool = InloopTool(InputParameters())
        inlooptool.import_surfaces(file_path=source)
        bgt_surfaces_qgis_vector_layer = as_qgis_memory_layer(
            inlooptool._database.bgt_surfaces,
            "BGT Oppervlakken"
        )
        bgt_surfaces_qgis_vector_layer.loadNamedStyle(BGT_STYLE)
        QgsProject.instance().addMapLayer(bgt_surfaces_qgis_vector_layer)

        return {self.OUTPUT: ""}
