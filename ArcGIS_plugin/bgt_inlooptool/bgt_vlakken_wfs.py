"""
Script Name: bgt inloop tool voor ArcGIS
Description: bgt inloop tool voor ArcGIS
Created By: Sjoerd Hoekstra
Date: 29/09/2020
"""

import sys
import os
import arcpy

# Relative imports don't work well in arcgis, therefore paths are appended to sys
bgt_inlooptool_dir = os.path.dirname(__file__)
sys.path.append(bgt_inlooptool_dir)
sys.path.append(os.path.join(bgt_inlooptool_dir, 'core'))

# Set path to Generic modules
from cls_general_use import GeneralUse
from common import BaseTool, parameter


class BgtVlakkenWFS(BaseTool):

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
            parameter(displayName='BAG (als geopackage)',
                      name='bag',
                      datatype="DEDatasetType",
                      parameterType="Optional",
                      direction="Input",
                      defaultValue=r"C:\GIS\test_data_inlooptool\bag.gpkg"),
        ]

        return self.parameters

    def updateParameters(self, parameters):

        super(BgtVlakkenWFS, self).updateParameters(parameters)

    def updateMessages(self, parameters):

        super(BgtVlakkenWFS, self).updateMessages(parameters)

    def execute(self, parameters, messages):
        try:
            self.arcgis_com = GeneralUse(sys, arcpy)
            self.arcgis_com.StartAnalyse()
            self.arcgis_com.AddMessage("Start BGT Inlooptool!")

            building_file = parameters[0].valueAsText

        except Exception:
            self.arcgis_com.Traceback()
        finally:
            self.arcgis_com.AddMessage("Klaar")
        return


if __name__ == '__main__':
    # This is used for debugging. Using this separated structure makes it much
    # easier to debug using standard Python development tools.

    try:
        tool = BgtVlakkenWFS()
        params = tool.getParameterInfo()

        # bag_file
        params[0].value = r"C:\GIS\test_data_inlooptool\bag.gpkg"

        tool.execute(parameters=params, messages=None)

    except Exception as ex:
        print('iets ging fout!')
