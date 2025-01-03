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
sys.path.append(os.path.join(bgt_inlooptool_dir, "core"))

# Set path to Generic modules
from cls_general_use import GeneralUse
from common import BaseTool, parameter, get_wkt_extent
from get_bgt_api_surfaces import get_bgt_api_surfaces


class DownloadBGTVlakken(BaseTool):
    def __init__(self):
        """
        Initialization.

        """
        self.label = "1. Download de BGT vlakken van PDOK"
        self.description = """Download de BGT vlakken van PDOK"""
        self.canRunInBackground = True

    def getParameterInfo(self):
        """return Parameter definitions."""
        """Create your parameters here using the paramater function.
        Make sure you leave the enclosing brackets and separate your
        parameters using commas.
        parameter(displayName, name, datatype, defaultValue=None, parameterType='Required', direction='Input')
        """

        self.parameters = [
            parameter(
                displayName="Interesse gebied als polygon",
                name="interesse_gebied",
                datatype="GPFeatureLayer",
                parameterType="Required",
                direction="Input",
            ),
            parameter(
                displayName="BGT download als zipfile van PDOK",
                name="bgt_zip",
                datatype="DEFile",
                parameterType="Required",
                direction="Output",
            ),
        ]
        return self.parameters

    def updateParameters(self, parameters):
        """
        updates a parameter in the interface if specified
        """
        if parameters[1].altered:
            # TODO pad default naar projectmap
            if "." in parameters[1].valueAsText:
                parameters[1].value = parameters[1].valueAsText.split(".")[0] + ".zip"
            else:
                parameters[1].value = parameters[1].valueAsText + ".zip"

        super(DownloadBGTVlakken, self).updateParameters(parameters)

    def updateMessages(self, parameters):
        """
        returns messages in the interface the wrong paths are filled in for the different parameters
        """
        # Messages interesse gebied
        if parameters[0].altered:
            desc = arcpy.Describe(parameters[0].valueAsText)
            if desc.dataType not in ["FeatureClass", "FeatureLayer", "ShapeFile"]:
                parameters[0].setErrorMessage(
                    "De invoer is niet van het type featureclass/shapefile/gpkg layer!"
                )
            else:
                if desc.shapeType != "Polygon":
                    parameters[0].setErrorMessage(
                        "De featureclass/shapefile/gpkg layer is niet van het type polygoon!"
                    )
                else:
                    feature_count = int(
                        arcpy.management.GetCount(parameters[0].valueAsText).getOutput(
                            0
                        )
                    )
                    if feature_count != 1:
                        parameters[0].setErrorMessage(
                            "Er is meer of minder dan 1 feature aanwezig of geselecteerd!"
                        )

        # Messages output BGT zipfile
        if parameters[1].altered:
            if os.path.exists(parameters[1].valueAsText):
                parameters[1].setWarningMessage(
                    "Het output bestand bestaat al, kies een nieuwe naam!"
                )

        super(DownloadBGTVlakken, self).updateMessages(parameters)

    def execute(self, parameters, messages):
        try:
            self.arcgis_com = GeneralUse(sys, arcpy)
            self.arcgis_com.StartAnalyse()
            self.arcgis_com.AddMessage("Start downloading BGT from PDOK!")

            input_area = parameters[0].valueAsText
            bgt_zip = parameters[1].valueAsText

            # get the input extent as wkt from the input_area
            extent_wkt = get_wkt_extent(input_area)
            get_bgt_api_surfaces(extent_wkt, bgt_zip)

        except Exception:
            self.arcgis_com.Traceback()
        finally:
            self.arcgis_com.AddMessage("Klaar")
        return


if __name__ == "__main__":
    # This is used for debugging. Using this separated structure makes it much
    # easier to debug using standard Python development tools.

    try:
        tool = DownloadBGTVlakken()
        params = tool.getParameterInfo()

        # bag_file
        params[
            0
        ].value = r"C:\Users\hsc\OneDrive - Tauw Group bv\ArcGIS\Projects\bgt_inlooptool\dokkum\ws.gdb\zwolle"
        params[
            1
        ].value = r"C:\Users\hsc\OneDrive - Tauw Group bv\ArcGIS\Projects\bgt_inlooptool\dokkum\nieuwe_plek.zip"

        tool.execute(parameters=params, messages=None)

    except Exception as ex:
        print("iets ging fout!")
