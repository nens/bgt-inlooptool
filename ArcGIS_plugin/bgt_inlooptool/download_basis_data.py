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


def enable_disable_options(parameters, bool_idx, input_field_idx):
    if parameters[bool_idx].value is True:
        parameters[input_field_idx].enabled = True
        parameters[input_field_idx].parameterType = "Required"
    else: 
        parameters[input_field_idx].enabled = False
        parameters[input_field_idx].parameterType = None

def add_zip_to_path(parameters, input_field_idx):
    if parameters[input_field_idx].altered:
        # TODO pad default naar projectmap
        if "." in parameters[1].valueAsText:
            parameters[input_field_idx].value = parameters[input_field_idx].valueAsText.split(".")[0] + ".zip"
        else:
            parameters[input_field_idx].value = parameters[input_field_idx].valueAsText + ".zip"

def check_if_file_already_exists(parameters, input_field_idx):
    if parameters[input_field_idx].altered:
        if os.path.exists(parameters[input_field_idx].valueAsText):
            parameters[input_field_idx].setWarningMessage(
                "Het outputbestand bestaat al, kies een nieuwe naam!"
            )
        else:
            parameters[input_field_idx].clearMessage()

class DownloadBasisData(BaseTool):
    def __init__(self):
        """
        Initialization.

        """
        self.label = "1. Download de basis data"
        self.description = """Download de basis data benodigd voor de tool"""
        self.canRunInBackground = True

        parameter_names = ["interesse_gebied", "bgt_download_bool", "bgt_zip_path", "gwsw_download_bool", "gwsw_zip_path", "bag_download_bool", "bag_zip_path"]

        self.search_area_idx = parameter_names.index("interesse_gebied")
        self.bgt_download_bool_idx = parameter_names.index("bgt_download_bool")
        self.bgt_storage_path_idx = parameter_names.index("bgt_zip_path")
        self.gwsw_download_bool_idx = parameter_names.index("gwsw_download_bool")
        self.gwsw_storage_path_idx = parameter_names.index("gwsw_zip_path")
        self.bag_download_bool_idx = parameter_names.index("bag_download_bool")
        self.bag_storage_path_idx = parameter_names.index("bag_zip_path")

    def getParameterInfo(self):
        """return Parameter definitions."""
        """Create your parameters here using the paramater function.
        Make sure you leave the enclosing brackets and separate your
        parameters using commas.
        parameter(displayName, name, datatype, defaultValue=None, parameterType='Required', direction='Input')
        """

        search_area = parameter(
            displayName="Interesse gebied als polygon",
            name="interesse_gebied",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input",
        )
        
        bgt_download_bool = parameter(
            displayName="Download BGT",
            name="bgt_download_bool",
            datatype="GPBoolean",
            parameterType="Required",
            direction="Input",
        )
        bgt_download_bool.value = True

        bgt_storage_path =  parameter(
            displayName="BGT download als zipfile van PDOK",
            name="bgt_zip_path",
            datatype="DEFile",
            parameterType="Required",
            direction="Output",
        )

        gwsw_download_bool = parameter(
            displayName="Download GWSW leidingen",
            name="gwsw_download_bool",
            datatype="GPBoolean",
            parameterType="Required",
            direction="Input",
        )
        gwsw_download_bool.value = True

        gwsw_storage_path =  parameter(
            displayName="GWSW download als zipfile van PDOK",
            name="gwsw_zip_path",
            datatype="DEFile",
            parameterType="Required",
            direction="Output",
        )

        bag_download_bool = parameter(
            displayName="Download BAG panden",
            name="bag_download_bool",
            datatype="GPBoolean",
            parameterType="Required",
            direction="Input",
        )
        bag_download_bool.value = True

        bag_storage_path =  parameter(
            displayName="BAG panden download als zipfile van PDOK",
            name="bag_zip_path",
            datatype="DEFile",
            parameterType="Required",
            direction="Output",
        )
        
        
        return [search_area, bgt_download_bool, bgt_storage_path, gwsw_download_bool, gwsw_storage_path, bag_download_bool, bag_storage_path]

    def updateParameters(self, parameters):
        """
        updates a parameter in the interface if specified
        """

        # Set correct path
        add_zip_to_path(parameters, self.bgt_storage_path_idx)
        add_zip_to_path(parameters, self.gwsw_storage_path_idx)
        add_zip_to_path(parameters, self.bag_storage_path_idx)

        # Enable/disable BGT parameters
        enable_disable_options(parameters, self.bgt_download_bool_idx, self.bgt_storage_path_idx)

        # Enable/disable GWSW parameters
        enable_disable_options(parameters, self.gwsw_download_bool_idx, self.gwsw_storage_path_idx)

        # Enable/disable BAG parameters
        enable_disable_options(parameters, self.bag_download_bool_idx, self.bag_storage_path_idx)
       
        super(DownloadBasisData, self).updateParameters(parameters)

    def updateMessages(self, parameters):
        """
        returns messages in the interface the wrong paths are filled in for the different parameters
        """
        # Messages interesse gebied
        if parameters[self.search_area_idx].altered:
            desc = arcpy.Describe(parameters[self.search_area_idx].valueAsText)
            if desc.dataType not in ["FeatureClass", "FeatureLayer", "ShapeFile"]:
                parameters[self.search_area_idx].setErrorMessage(
                    "De invoer is niet van het type featureclass/shapefile/gpkg layer!"
                )
            else:
                if desc.shapeType != "Polygon":
                    parameters[self.search_area_idx].setErrorMessage(
                        "De featureclass/shapefile/gpkg layer is niet van het type polygoon!"
                    )
                else:
                    feature_count = int(
                        arcpy.management.GetCount(parameters[self.search_area_idx].valueAsText).getOutput(
                            self.search_area_idx
                        )
                    )
                    if feature_count != 1:
                        parameters[self.search_area_idx].setErrorMessage(
                            "Er is meer of minder dan 1 feature aanwezig of geselecteerd!"
                        )

        # Validate zip files
        check_if_file_already_exists(parameters, self.bgt_storage_path_idx)
        check_if_file_already_exists(parameters, self.gwsw_storage_path_idx)
        check_if_file_already_exists(parameters, self.bag_storage_path_idx)


        super(DownloadBasisData, self).updateMessages(parameters)

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
        tool = DownloadBasisData()
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
