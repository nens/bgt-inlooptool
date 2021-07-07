"""
Script Name: Download de BGT vlakken van PDOK
Description: Download de BGT vlakken van PDOK
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
from get_bgt_api_surfaces import get_bgt_api_surfaces


class DownloadBGTVlakken(BaseTool):

    def __init__(self):
        """
        Initialization.

        """
        self.label = '1. Download de BGT vlakken van PDOK'
        self.description = '''Download de BGT vlakken van PDOK'''
        self.canRunInBackground = True

    def getParameterInfo(self):
        """ return Parameter definitions."""
        '''Create your parameters here using the paramater function.
        Make sure you leave the enclosing brackets and separate your
        parameters using commas.
        parameter(displayName, name, datatype, defaultValue=None, parameterType='Required', direction='Input')
        '''

        self.parameters = [
            parameter(displayName='Interesse gebied als polygon',
                      name='interesse_gebied',
                      datatype="GPFeatureLayer",
                      parameterType="Required",
                      direction="Input"),
            parameter(displayName='BGT download als zipfile van PDOK',
                      name='bgt_zip',
                      datatype="DEFile",
                      parameterType="Required",
                      direction="Output")
        ]
        return self.parameters

    def updateParameters(self, parameters):

        super(DownloadBGTVlakken, self).updateParameters(parameters)

    def updateMessages(self, parameters):

        # Messages interesse gebied
        if parameters[0].altered:
            desc = arcpy.Describe(parameters[0].valueAsText)
            if desc.dataType not in ['FeatureClass', 'FeatureLayer', 'ShapeFile']:
                parameters[0].setErrorMessage('De invoer is niet van het type featureclass/shapefile/gpkg layer!')
            else:
                if desc.shapeType != 'Polygon':
                    parameters[0].setErrorMessage('De featureclass/shapefile/gpkg layer is niet van het type polygoon!')
                else:
                    feature_count = int(arcpy.management.GetCount(parameters[0].valueAsText).getOutput(0))
                    if feature_count != 1:
                        parameters[0].setErrorMessage('Er is meer of minder dan 1 feature aanwezig of geselecteerd!')

        # Messages output BGT zipfile
        if parameters[1].altered:
            if parameters[1].valueAsText[-4:].lower() != '.zip':
                parameters[1].setErrorMessage('Het output bestand is geen zipfile! Zorg dat dit wel een zipfile is!')
            else:
                if os.path.exists(parameters[1].valueAsText):
                    parameters[1].setWarningMessage('Het output bestand bestaat al, kies een nieuwe naam!')

        super(DownloadBGTVlakken, self).updateMessages(parameters)

    def execute(self, parameters, messages):
        try:
            self.arcgis_com = GeneralUse(sys, arcpy)
            self.arcgis_com.StartAnalyse()
            self.arcgis_com.AddMessage("Start downloading BGT from PDOK!")

            input_area = parameters[0].valueAsText
            bgt_zip = parameters[1].valueAsText

            with arcpy.da.SearchCursor(input_area, ['Shape@WKT']) as cursor:
                for row in cursor:
                    extent_wkt = row[0]

            get_bgt_api_surfaces(extent_wkt, bgt_zip)

        except Exception:
            self.arcgis_com.Traceback()
        finally:
            self.arcgis_com.AddMessage("Klaar")
        return


if __name__ == '__main__':
    # This is used for debugging. Using this separated structure makes it much
    # easier to debug using standard Python development tools.

    try:
        tool = DownloadBGTVlakken()
        params = tool.getParameterInfo()

        # bag_file
        params[0].value = r"C:\Users\hsc\OneDrive - Tauw Group bv\ArcGIS\Projects\bgt_inlooptool\dokkum\ws.gdb\zwolle"
        params[1].value = r"C:\Users\hsc\OneDrive - Tauw Group bv\ArcGIS\Projects\bgt_inlooptool\dokkum\test_bgt_output"

        tool.execute(parameters=params, messages=None)

    except Exception as ex:
        print('iets ging fout!')
