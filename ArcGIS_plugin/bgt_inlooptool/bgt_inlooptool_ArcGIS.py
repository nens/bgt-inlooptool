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
sys.path.append(os.path.join(bgt_inlooptool_dir, "core"))

# Set path to Generic modules
from cls_general_use import GeneralUse
from common import BaseTool, parameter, get_wkt_extent, layers_to_gdb
from common import add_bgt_inlooptabel_symbologyfield, add_gwsw_symbologyfield
from visualize_layers import VisualizeLayers

# import bgt inlooptool
from core.inlooptool import InloopTool, InputParameters
from core.defaults import (
    MAX_AFSTAND_VLAK_AFWATERINGSVOORZIENING,
    MAX_AFSTAND_VLAK_OPPWATER,
    MAX_AFSTAND_PAND_OPPWATER,
    MAX_AFSTAND_VLAK_KOLK,
    MAX_AFSTAND_AFGEKOPPELD,
    MAX_AFSTAND_DRIEVOUDIG,
    AFKOPPELEN_HELLENDE_DAKEN,
    BOUWJAAR_GESCHEIDEN_BINNENHUISRIOLERING,
    VERHARDINGSGRAAD_ERF,
    VERHARDINGSGRAAD_HALF_VERHARD,
)


class BGTInloopToolArcGIS(BaseTool):
    def __init__(self):
        """
        Initialization.
        """
        self.label = "2. BGT Inlooptool"
        self.description = """BGT inlooptool voor ArcGIS"""
        self.canRunInBackground = True
        self.arcgis_com = GeneralUse(sys, arcpy)

    def getParameterInfo(self):
        """return Parameter definitions."""
        """Create your parameters here using the paramater function.
        Make sure you leave the enclosing brackets and separate your
        parameters using commas.
        parameter(displayName, name, datatype, defaultValue=None, parameterType='Required', direction='Input')
        """
        layers = os.path.join(os.path.dirname(__file__), "layers")

        parameters = [
            parameter(
                displayName="BGT (als zipfile)",
                name="bgt",
                datatype="DEFile",
                parameterType="Required",
                direction="Input",
            ),
            parameter(
                displayName="GWSW Leidingen (als geopackage)",
                name="leidingen",
                datatype="DEDatasetType",
                parameterType="Required",
                direction="Input",
            ),
            parameter(
                displayName="BAG (als geopackage)",
                name="bag",
                datatype="DEDatasetType",
                parameterType="Optional",
                direction="Input",
            ),
            parameter(
                displayName="Kolken",
                name="kolken_file",
                datatype="GPFeatureLayer",
                parameterType="Optional",
                direction="Input",
            ),
            parameter(
                displayName="Analyse gebied",
                name="input_extent_mask_wkt",
                datatype="GPFeatureLayer",
                parameterType="Optional",
                direction="Input",
            ),
            parameter(
                displayName="Opslag locatie gpkg",
                name="output_gpkg",
                datatype="DEDatasetType",
                parameterType="Required",
                direction="Output",
            ),
            parameter(
                displayName="maximale afstand vlak afwateringsvoorziening",
                name="max_vlak_afwatervoorziening",
                datatype="GPDouble",
                parameterType="Required",
                direction="Input",
                defaultValue=MAX_AFSTAND_VLAK_AFWATERINGSVOORZIENING,
            ),
            parameter(
                displayName="maximale afstand vlak oppervlaktewater",
                name="max_vlak_oppwater",
                datatype="GPDouble",
                parameterType="Required",
                direction="Input",
                defaultValue=MAX_AFSTAND_VLAK_OPPWATER,
            ),
            parameter(
                displayName="maximale afstand pand oppervlaktewater",
                name="max_pand_opwater",
                datatype="GPDouble",
                parameterType="Required",
                direction="Input",
                defaultValue=MAX_AFSTAND_PAND_OPPWATER,
            ),
            parameter(
                displayName="maximale afstand vlak kolk",
                name="max_vlak_kolk",
                datatype="GPDouble",
                parameterType="Required",
                direction="Input",
                defaultValue=MAX_AFSTAND_VLAK_KOLK,
            ),
            parameter(
                displayName="maximale afstand afgekoppeld",
                name="max_afgekoppeld",
                datatype="GPDouble",
                parameterType="Required",
                direction="Input",
                defaultValue=MAX_AFSTAND_AFGEKOPPELD,
            ),
            parameter(
                displayName="maximale afstand drievoudig",
                name="max_drievoudig",
                datatype="GPDouble",
                parameterType="Required",
                direction="Input",
                defaultValue=MAX_AFSTAND_DRIEVOUDIG,
            ),
            parameter(
                displayName="afkoppelen hellende daken",
                name="afkoppelen_daken",
                datatype="GPBoolean",
                parameterType="Required",
                direction="Input",
                defaultValue=AFKOPPELEN_HELLENDE_DAKEN,
            ),
            parameter(
                displayName="bouwjaar gescheiden binnenhuisriolering",
                name="bouwjaar_riool",
                datatype="GPLong",
                parameterType="Required",
                direction="Input",
                defaultValue=BOUWJAAR_GESCHEIDEN_BINNENHUISRIOLERING,
            ),
            parameter(
                displayName="verhardingsgraad erf",
                name="verhardingsgraaf_erf",
                datatype="GPDouble",
                parameterType="Required",
                direction="Input",
                defaultValue=VERHARDINGSGRAAD_ERF,
            ),
            parameter(
                displayName="verhardingsgraad half verhard",
                name="verhardingsgraad_half_verhard",
                datatype="GPDouble",
                parameterType="Required",
                direction="Input",
                defaultValue=VERHARDINGSGRAAD_HALF_VERHARD,
            ),
            parameter(
                displayName="BGT oppervlakken symbology",
                name="bgt_oppervlakken_symb",
                datatype="GPLayer",
                parameterType="Derived",
                direction="Output",
                symbology=os.path.join(layers, "bgt_oppervlakken.lyrx"),
            ),
            parameter(
                displayName="BGT Inlooptabel symoblogy",
                name="bgt_inlooptabel_symb",
                datatype="GPLayer",
                parameterType="Derived",
                direction="Output",
                symbology=os.path.join(layers, "bgt_inlooptabel.lyrx"),
            ),
            parameter(
                displayName="GWSW lijnen symbology",
                name="gwsw_lijn_symb",
                datatype="GPLayer",
                parameterType="Derived",
                direction="Output",
                symbology=os.path.join(layers, "gwsw_lijn.lyrx"),
            ),
        ]

        return parameters

    def updateParameters(self, parameters):
        """
        updates a parameter in the interface if specified
        """
        output_gpkg = parameters[5]
        if output_gpkg.altered:
            # TODO pad default naar projectmap
            if "." in output_gpkg.valueAsText:
                output_gpkg.value = output_gpkg.valueAsText.split(".")[0] + ".gpkg"
            else:
                output_gpkg.value = output_gpkg.valueAsText + ".gpkg"

        super(BGTInloopToolArcGIS, self).updateParameters(parameters)

    def updateMessages(self, parameters):
        """
        returns messages in the interface the wrong paths are filled in for the different parameters
        """
        bgt_file = parameters[0]
        pipe_file = parameters[1]
        bag_file = parameters[2]
        input_area = parameters[4]

        if bgt_file.altered:
            if bgt_file.valueAsText[-4:].lower() != ".zip":
                bgt_file.setErrorMessage(
                    "De input voor bgt data moet een zip file zijn met .gml files"
                )

        if pipe_file.altered:
            if pipe_file.valueAsText[-5:].lower() != ".gpkg":
                pipe_file.setErrorMessage(
                    "De input voor leidingen data moet een geopackage (.gpkg) zijn"
                )

        if bag_file.altered:
            if bag_file.valueAsText[-5:].lower() != ".gpkg":
                bag_file.setErrorMessage(
                    "De input voor bag data moet een geopackage (.gpkg) zijn"
                )

        # Messages interesse gebied
        if input_area.altered:
            desc = arcpy.Describe(input_area.valueAsText)
            if desc.dataType not in ["FeatureClass", "FeatureLayer", "ShapeFile"]:
                input_area.setErrorMessage(
                    "De invoer is niet van het type featureclass/shapefile/gpkg layer!"
                )
            else:
                if desc.shapeType != "Polygon":
                    input_area.setErrorMessage(
                        "De featureclass/shapefile/gpkg layer is niet van het type polygoon!"
                    )
                else:
                    feature_count = int(
                        arcpy.management.GetCount(input_area.valueAsText).getOutput(0)
                    )
                    if feature_count != 1:
                        input_area.setErrorMessage(
                            "Er is meer of minder dan 1 feature aanwezig of geselecteerd!"
                        )

        super(BGTInloopToolArcGIS, self).updateMessages(parameters)

    def execute(self, parameters, messages):
        try:
            self.arcgis_com.StartAnalyse()
            self.arcgis_com.AddMessage("Start BGT Inlooptool!")

            bgt_file = parameters[0].valueAsText
            pipe_file = parameters[1].valueAsText
            building_file = parameters[2].valueAsText
            kolken_file = parameters[3].valueAsText
            input_area = parameters[4].valueAsText
            output_gpkg = parameters[5].valueAsText

            core_parameters = InputParameters(
                max_afstand_vlak_afwateringsvoorziening=parameters[6].value,
                max_afstand_vlak_oppwater=parameters[7].value,
                max_afstand_pand_oppwater=parameters[8].value,
                max_afstand_vlak_kolk=parameters[9].value,
                max_afstand_afgekoppeld=parameters[10].value,
                max_afstand_drievoudig=parameters[11].value,
                afkoppelen_hellende_daken=parameters[12].value,
                gebruik_bag=building_file != None,
                gebruik_kolken=kolken_file != None,
                bouwjaar_gescheiden_binnenhuisriolering=parameters[13].value,
                verhardingsgraad_erf=parameters[14].value,
                verhardingsgraad_half_verhard=parameters[15].value,
            )

            # Output layers
            bgt_oppervlakken_symb = parameters[16]
            bgt_inlooptabel_symb = parameters[17]
            gwsw_lijn_symb = parameters[18]

            # start of the core
            inlooptool = InloopTool(core_parameters)
            # Import surfaces and pipes
            self.arcgis_com.AddMessage("Importeren van BGT bestanden")
            inlooptool.import_surfaces(bgt_file)
            self.arcgis_com.AddMessage("Importeren van GWSW bestanden")
            inlooptool.import_pipes(pipe_file)

            if core_parameters.gebruik_kolken:
                self.arcgis_com.AddMessage("Importeren van kolken bestanden")
                inlooptool.import_kolken(kolken_file)
            inlooptool._database.add_index_to_inputs(
                kolken=core_parameters.gebruik_kolken
            )

            if core_parameters.gebruik_bag:
                self.arcgis_com.AddMessage("Importeren van BAG gebouw bestanden")
                inlooptool._database.add_build_year_to_surface(file_path=building_file)

            if input_area is not None:
                # get the input extent as wkt from the input_area
                input_extent_mask_wkt = get_wkt_extent(input_area)

                inlooptool._database.remove_input_features_outside_clip_extent(
                    input_extent_mask_wkt
                )
                inlooptool._database.add_index_to_inputs(
                    kolken=core_parameters.gebruik_kolken
                )

            self.arcgis_com.AddMessage("Afstanden aan het berekenen")
            inlooptool.calculate_distances(parameters=core_parameters)
            self.arcgis_com.AddMessage("Bereken Runoff targets")
            inlooptool.calculate_runoff_targets()

            # Export results
            self.arcgis_com.AddMessage("Exporteren naar GPKG")
            inlooptool._database._write_to_disk(output_gpkg)

            # Add layers to the map
            self.arcgis_com.AddMessage("Visualiseren van resultaten!")
            out_gdb = output_gpkg.replace(".gpkg", ".gdb")
            # add symbology field for bgt_inlooptabel
            main_bgt_inlooptabel = layers_to_gdb(
                input_dataset=os.path.join(output_gpkg, "main.bgt_inlooptabel"),
                output_gdb=out_gdb,
            )
            add_bgt_inlooptabel_symbologyfield(main_bgt_inlooptabel)
            bgt_oppervlakken_symb.value = main_bgt_inlooptabel
            bgt_inlooptabel_symb.value = main_bgt_inlooptabel

            # add symbology field for GWSW lijnen
            main_default_lijn = layers_to_gdb(
                input_dataset=os.path.join(pipe_file, "main.default_lijn"),
                output_gdb=out_gdb,
            )
            add_gwsw_symbologyfield(main_default_lijn)
            gwsw_lijn_symb.value = main_default_lijn

            visualize_layers = VisualizeLayers()
            for x, layer_parameter in enumerate(
                [bgt_oppervlakken_symb, bgt_inlooptabel_symb, gwsw_lijn_symb], 16
            ):
                visualize_layers.add_layer_to_map(in_param=layer_parameter, param_nr=x)
            visualize_layers.save()

        except Exception:
            self.arcgis_com.Traceback()
        finally:
            self.arcgis_com.AddMessage("Klaar")
        return


if __name__ == "__main__":
    # This is used for debugging. Using this separated structure makes it much
    # easier to debug using standard Python development tools.

    try:
        tool = BGTInloopToolArcGIS()
        params = tool.getParameterInfo()

        main_path = r"C:\Users\vdi\OneDrive - TAUW Group bv\Werkzaamheden\1287914 - BGT inlooptool\testdata2"
        # bgt_file
        params[0].value = os.path.join(main_path, "BGT_Akersloot2.zip")
        # pipe_file
        params[1].value = os.path.join(main_path, "getGeoPackage_1934.gpkg")
        # bag_file
        params[2].value = os.path.join(main_path, "BAG_Akersloot.gpkg")
        # kolken_file
        params[3].value = os.path.join(main_path, "kolken_Castricum_Limmen_Akersloot.shp")
        # area_file
        params[4].value = os.path.join(main_path, "extent_Akersloot.shp")  #os.path.join(main_path, r"polyoon_centrum.gdb\Polygoon_centrum")
        # output_location
        params[5].value = os.path.join(main_path, "output.gpkg")

        # maximale afstand vlak afwateringsvoorziening
        params[6].value = 40
        # maximale afstand vlak oppervlaktewater
        params[7].value = 2
        # maximale afstand pand oppervlaktewater
        params[8].value = 6
        # 'maximale afstand vlak kolk
        params[9].value = 30
        # maximale afstand afgekoppeld
        params[10].value = 3
        # maximale afstand drievoudig
        params[11].value = 4
        # afkoppelen hellende daken
        params[12].value = True
        # bouwjaar gescheiden binnenhuisriolering
        params[13].value = 1992
        # verhardingsgraad erf
        params[14].value = 50
        # verhardingsgraad half verhard
        params[15].value = 50

        tool.execute(parameters=params, messages=None)

    except Exception as ex:
        print("iets ging fout!")
