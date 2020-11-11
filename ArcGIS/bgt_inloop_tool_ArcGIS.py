"""
Script Name: bgt inloop tool voor ArcGIS
Description: bgt inloop tool voor ArcGIS
Created By: Sjoerd Hoekstra
Date: 29/09/2020
"""

import sys
import os
if 'python.exe' in sys.executable:
    import arcview  # or arceditor, arcinfo
import arcpy

# Set path to Generic modules
import clsGeneralUse
from common import BaseTool, parameter

# import bgt inlooptool
# from inlooptool import BGTInloopTool
# from test_inlooptool import UnitDatabase


class BGTInloopToolArcGIS(BaseTool):
    def __init__(self):
        """
        Initialization.

        """
        self.label = 'bgt inloop tool voor ArcGIS'
        self.description = '''bgt inloop tool voor ArcGIS'''
        self.canRunInBackground = True

    def getParameterInfo(self):
        """ return Parameter definitions."""
        '''Create your parameters here using the paramater function.
        Make sure you leave the enclosing brackets and separate your
        parameters using commas.
        parameter(displayName, name, datatype, defaultValue=None, parameterType='Required', direction='Input')
        '''
        # TODO volgende fase ook importeren als GDB of shapefiles
        self.parameters = [
            parameter('BAG (als geopackage)', 'bag', "DEDatasetType", parameterType="Required", direction="Input"),
            parameter('BGT (als zipfile)', 'bgt', "DEFile", parameterType="Required", direction="Input"),
            parameter('Leidingen (als geopackage)', 'leidingen', 'DEDatasetType', parameterType='Required',
                      direction='Input')
            ]
        # DEFILE en GPType werken niet
        return self.parameters

    def updateParameters(self, parameters):

        super(BGTInloopToolArcGIS, self).updateParameters(parameters)

    def updateMessages(self, parameters):

        bag = parameters[0]
        bgt = parameters[1]
        leidingen = parameters[2]

        if bag.altered:
            if bag.valueAsText[-5:] != ".gpkg":
                bag.setErrorMessage('De input voor bag data moet een geopackage (.gpkg) zijn')

        if bgt.altered:
            if bgt.valueAsText[-4:] != ".zip":
                bgt.setErrorMessage('De input voor bgt data moet een zip file zijn met .gml files')

        if leidingen.altered:
            if leidingen.valueAsText[-5:] != ".gpkg":
                leidingen.setErrorMessage('De input voor leidingen data moet een geopackage (.gpkg) zijn')

        super(BGTInloopToolArcGIS, self).updateMessages(parameters)

    def execute(self, parameters, messages):
        try:
            self.arcgis_com = clsGeneralUse.TT_GeneralUse(sys, arcpy)
            self.arcgis_com.StartAnalyse()

            bag = parameters[0].value
            bgt = parameters[1].value
            leidingen = parameters[2].valueAsText

            # inloop_obj = BGTInloopTool(BAG_input, BGT_input, Leidingen_input, self.arcgis_com)

        except Exception:
            self.arcgis_com.Traceback()
        finally:
            self.arcgis_com.AddMessage("Klaar")
        return


if __name__ == '__main__':
    # This is used for debugging. Using this separated structure makes it much
    # easier to debug using standard Python development tools.

    tool = BGTInloopToolArcGIS()
    params = tool.getParameterInfo()

    # param0
    params[0].value = "test.shp"
    # param1
    params[1].value = "iets.zip2"
    # param2
    params[2].value = 'ja.gpkg2'

    tool.execute(parameters=params, messages=None)
