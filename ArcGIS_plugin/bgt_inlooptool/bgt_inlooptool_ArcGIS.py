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
from clsGeneralUse import TT_GeneralUse
from common import BaseTool, parameter

# import bgt inlooptool
# core = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'core')
# sys.path.append(core)
from core.inlooptool import InloopTool
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
            parameter('BAG (als geopackage)', 'bag', "DEDatasetType",
                      parameterType="Required", direction="Input"),
            parameter('BGT (als zipfile)', 'bgt', "DEFile",
                      parameterType="Required", direction="Input"),
            parameter('Leidingen (als geopackage)', 'leidingen', 'DEDatasetType',
                      parameterType='Required', direction='Input'),
            parameter('maximale afstand vlak afwateringsvoorziening', 'max_vlak_afwatervoorziening', 'INTEGER',
                      parameterType='Required', direction='Input'),
            parameter('maximale afstand vlak oppervlaktewater', 'max_vlak_oppwater', 'INTEGER',
                      parameterType='Required', direction='Input'),
            parameter('maximale afstand pand oppervlaktewater', 'max_pand_opwater', 'INTEGER',
                      parameterType='Required', direction='Input'),
            parameter('maximale afstand vlak kolk', 'max_vlak_kolk', 'INTEGER',
                      parameterType='Required', direction='Input'),
            parameter('maximale afstand afgekoppeld', 'max_afgekoppeld', 'INTEGER',
                      parameterType='Required', direction='Input'),
            parameter('maximale afstand drievoudig', 'max_drievoudig', 'INTEGER',
                      parameterType='Required', direction='Input'),
            parameter('afkoppelen hellende daken', 'afkoppelen_daken', 'GPBoolean',
                      parameterType='Required', direction='Input'),
            parameter('bouwjaar gescheiden binnenhuisriolering', 'bouwjaar_riool', 'INTEGER',
                      parameterType='Required', direction='Input'),
            parameter('verhardingsgraad erf', 'verhardingsgraaf_erf', 'INTEGER',
                      parameterType='Required', direction='Input'),
            parameter('verhardingsgraad half verhard', 'verhardingsgraad_half_verhard', 'INTEGER',
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

            # max_vlak_afwatervoorziening = parameters[3].value
            # max_vlak_oppwater = parameters[4].value
            # max_pand_opwater = parameters[5].value
            # max_vlak_kolk = parameters[6].value
            # max_afgekoppeld = parameters[7].value
            # max_drievoudig = parameters[8].value
            # afkoppelen_daken = parameters[9].value
            # bouwjaar_riool = parameters[10].value
            # verhardingsgraaf_erf = parameters[11].value
            # verhardingsgraad_half_verhard = parameters[12].value

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

    # param0
    params[0].value = "test.shp"
    # param1
    params[1].value = "iets.zip2"
    # param2
    params[2].value = 'ja.gpkg2'

    tool.execute(parameters=params, messages=None)
