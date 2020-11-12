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
from clsGeneralUse import TT_GeneralUse
from common import BaseTool, parameter

# import bgt inlooptool
from inlooptool import InloopTool


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
            parameter('BAG (als geopackage)', 'bag', "DEDatasetType",
                      parameterType="Required", direction="Input"),
            parameter('BGT (als zipfile)', 'bgt', "DEFile",
                      parameterType="Required", direction="Input"),
            parameter('Leidingen (als geopackage)', 'leidingen', 'DEDatasetType',
                      parameterType='Required', direction='Input'),
            parameter('maximale afstand vlak afwateringsvoorziening', 'max_vlak_afwatervoorziening', 'GPLong',
                      parameterType='Required', direction='Input'),
            parameter('maximale afstand vlak oppervlaktewater', 'max_vlak_oppwater', 'GPLong',
                      parameterType='Required', direction='Input'),
            parameter('maximale afstand pand oppervlaktewater', 'max_pand_opwater', 'GPLong',
                      parameterType='Required', direction='Input'),
            parameter('maximale afstand vlak kolk', 'max_vlak_kolk', 'GPLong',
                      parameterType='Required', direction='Input'),
            parameter('maximale afstand afgekoppeld', 'max_afgekoppeld', 'GPLong',
                      parameterType='Required', direction='Input'),
            parameter('maximale afstand drievoudig', 'max_drievoudig', 'GPLong',
                      parameterType='Required', direction='Input'),
            parameter('afkoppelen hellende daken', 'afkoppelen_daken', 'GPBoolean',
                      parameterType='Required', direction='Input'),
            parameter('bouwjaar gescheiden binnenhuisriolering', 'bouwjaar_riool', 'GPLong',
                      parameterType='Required', direction='Input'),
            parameter('verhardingsgraad erf', 'verhardingsgraaf_erf', 'GPLong',
                      parameterType='Required', direction='Input'),
            parameter('verhardingsgraad half verhard', 'verhardingsgraad_half_verhard', 'GPLong',
                      parameterType='Required', direction='Input')
            ]

        return self.parameters

    def updateParameters(self, parameters):

        super(BGTInloopToolArcGIS, self).updateParameters(parameters)

    def updateMessages(self, parameters):

        bag_file = parameters[0]
        bgt_file = parameters[1]
        pipe_file = parameters[2]

        if bag_file.altered:
            if bag_file.valueAsText[-5:] != ".gpkg":
                bag_file.setErrorMessage('De input voor bag data moet een geopackage (.gpkg) zijn')

        if bgt_file.altered:
            if bgt_file.valueAsText[-4:] != ".zip":
                bgt_file.setErrorMessage('De input voor bgt data moet een zip file zijn met .gml files')

        if pipe_file.altered:
            if pipe_file.valueAsText[-5:] != ".gpkg":
                pipe_file.setErrorMessage('De input voor leidingen data moet een geopackage (.gpkg) zijn')

        super(BGTInloopToolArcGIS, self).updateMessages(parameters)

    def execute(self, parameters, messages):
        try:
            self.arcgis_com = TT_GeneralUse(sys, arcpy)
            self.arcgis_com.StartAnalyse()
            self.arcgis_com.AddMessage("Start analyse!")

            bag_file = parameters[0].value
            bgt_file = parameters[1].value
            pipe_file = parameters[2].valueAsText

            core_parameters = [parameters[x].value for x in range(3, 13)]
            self.it = InloopTool(core_parameters)

            # Import surfaces and pipes
            self.it.import_surfaces(bgt_file)
            self.it.import_pipes(pipe_file)

            self.it.calculate_distances(parameters=self.parameters, use_index=self.use_index)

            self.it.calculate_runoff_targets()

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

    # bag_file
    params[0].value = r"C:\Users\hsc\OneDrive - Tauw Group bv\Github\bgt-inlooptool\test-data\bag.gpkg"
    # bgt_file
    params[1].value = r"C:\Users\hsc\OneDrive - Tauw Group bv\Github\bgt-inlooptool\test-data\extract.zip"
    # pipe_file
    params[2].value = r"C:\Users\hsc\OneDrive - Tauw Group bv\Github\bgt-inlooptool\test-data\getGeoPackage_1134.gpkg"
    # maximale afstand vlak afwateringsvoorziening
    params[3].value = 40
    # maximale afstand vlak oppervlaktewater
    params[4].value = 2
    # maximale afstand pand oppervlaktewater
    params[5].value = 6
    # 'maximale afstand vlak kolk
    params[6].value = 30
    # maximale afstand afgekoppeld
    params[7].value = 3
    # maximale afstand drievoudig
    params[8].value = 4
    # afkoppelen hellende daken
    params[9].value = True
    # bouwjaar gescheiden binnenhuisriolering
    params[10].value = 1992
    # verhardingsgraad erf
    params[11].value = 50
    # verhardingsgraad half verhard
    params[11].value = 50

    tool.execute(parameters=params, messages=None)
