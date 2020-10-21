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
from test_inlooptool import UnitDatabase


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

        self.parameters = [
            parameter('AHN type', 'AHNtype', "String", parameterType="Required", direction="Input"),
            parameter('AHN versie', 'AHNversie', "String", parameterType="Required", direction="Input"),
            parameter('Gebiedsbegrenzing', 'InputArea', 'GPFeatureLayer', parameterType='Required', direction='Input')
            ]

        return self.parameters

    def updateParameters(self, parameters):

        super(BGTInloopToolArcGIS, self).updateParameters(parameters)

    def updateMessages(self, parameters):

        super(BGTInloopToolArcGIS, self).updateMessages(parameters)

    def execute(self, parameters, messages):
        try:
            self.arcgis_com = clsGeneralUse.TT_GeneralUse(sys, arcpy)
            self.arcgis_com.StartAnalyse()

            param0 = parameters[0].value
            param1 = parameters[1].value
            param2 = parameters[2].valueAsText

            inloop_obj = BGTInloopTool(self.arcgis_com)

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
    params[0].value = ""
    # param1
    params[1].value = ""
    # param2
    params[2].value = r''

    tool.execute(parameters=params, messages=None)
