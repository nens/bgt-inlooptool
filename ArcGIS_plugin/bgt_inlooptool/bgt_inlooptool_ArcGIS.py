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

        self.parameter_names = ["previous_results", "bgt", "leidingen", "bag", "kolken_file", "input_extent_mask_wkt", "input_statistics_shape", "output_gpkg", "max_vlak_afwatervoorziening", "max_vlak_oppwater",
                                "max_pand_opwater", "max_vlak_kolk", "max_afgekoppeld", "max_drievoudig", "afkoppelen_daken", "bouwjaar_riool", "verhardingsgraaf_erf",
                                "verhardingsgraad_half_verhard", "bgt_oppervlakken_symb", "bgt_inlooptabel_symb", "gwsw_lijn_symb", "copy_pipe_codes"]
        
        self.previous_results_idx = self.parameter_names.index("previous_results")
        self.bgt_idx = self.parameter_names.index("bgt")
        self.leidingen_idx = self.parameter_names.index("leidingen")
        self.bag_idx = self.parameter_names.index("bag")
        self.kolken_file_idx = self.parameter_names.index("kolken_file")
        self.input_extent_mask_wkt_idx = self.parameter_names.index("input_extent_mask_wkt")
        self.input_statistics_shape_idx = self.parameter_names.index("input_statistics_shape")
        self.output_gpkg_idx = self.parameter_names.index("output_gpkg")
        self.max_vlak_afwatervoorziening_idx = self.parameter_names.index("max_vlak_afwatervoorziening")
        self.max_vlak_oppwater_idx = self.parameter_names.index("max_vlak_oppwater")
        self.max_pand_opwater_idx = self.parameter_names.index("max_pand_opwater")
        self.max_vlak_kolk_idx = self.parameter_names.index("max_vlak_kolk")
        self.max_afgekoppeld_idx = self.parameter_names.index("max_afgekoppeld")
        self.max_drievoudig_idx = self.parameter_names.index("max_drievoudig")
        self.afkoppelen_daken_idx = self.parameter_names.index("afkoppelen_daken")
        self.bouwjaar_riool_idx = self.parameter_names.index("bouwjaar_riool")
        self.verhardingsgraaf_erf_idx = self.parameter_names.index("verhardingsgraaf_erf")
        self.verhardingsgraad_half_verhard_idx = self.parameter_names.index("verhardingsgraad_half_verhard")
        self.bgt_oppervlakken_symb_idx = self.parameter_names.index("bgt_oppervlakken_symb")
        self.bgt_inlooptabel_symb_idx = self.parameter_names.index("bgt_inlooptabel_symb")
        self.gwsw_lijn_symb_idx = self.parameter_names.index("gwsw_lijn_symb")
        self.copy_pipe_codes_idx = self.parameter_names.index("copy_pipe_codes")

    def getParameterInfo(self):
        """return Parameter definitions."""
        """Create your parameters here using the paramater function.
        Make sure you leave the enclosing brackets and separate your
        parameters using commas.
        parameter(displayName, name, datatype, defaultValue=None, parameterType='Required', direction='Input')
        """
        layers = os.path.join(os.path.dirname(__file__), "layers")

        previous_results =  parameter(
            displayName="Vorige tooluitkomsten (als geopackage)",
            name="previous_results",
            datatype="DEDatasetType",
            parameterType="Required",
            direction="Input",
        ),
        bgt = parameter(
            displayName="BGT (als zipfile)",
            name="bgt",
            datatype="DEFile",
            parameterType="Required",
            direction="Input",
        ),
        leidingen = parameter(
            displayName="GWSW Leidingen (als geopackage)",
            name="leidingen",
            datatype="DEDatasetType",
            parameterType="Required",
            direction="Input",
        ),
        bag = parameter(
            displayName="BAG (als geopackage)",
            name="bag",
            datatype="DEDatasetType",
            parameterType="Optional",
            direction="Input",
        ),
        kolken_file = parameter(
            displayName="Kolken",
            name="kolken_file",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input",
        ),
        input_extent_mask_wkt = parameter(
            displayName="Analysegebied",
            name="input_extent_mask_wkt",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input",
        ),
        input_statistics_shape = parameter(
            displayName="Statistiekgebieden",
            name="input_statistics_shape",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input",
        ),
        output_gpkg = parameter(
            displayName="Opslaglocatie gpkg",
            name="output_gpkg",
            datatype="DEDatasetType",
            parameterType="Required",
            direction="Output",
        ),
        max_vlak_afwatervoorziening = parameter(
            displayName="maximale afstand vlak afwateringsvoorziening",
            name="max_vlak_afwatervoorziening",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input",
            defaultValue=MAX_AFSTAND_VLAK_AFWATERINGSVOORZIENING,
        ),
        max_vlak_oppwater = parameter(
            displayName="maximale afstand vlak oppervlaktewater",
            name="max_vlak_oppwater",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input",
            defaultValue=MAX_AFSTAND_VLAK_OPPWATER,
        ),
        max_pand_opwater = parameter(
            displayName="maximale afstand pand oppervlaktewater",
            name="max_pand_opwater",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input",
            defaultValue=MAX_AFSTAND_PAND_OPPWATER,
        ),
        max_vlak_kolk = parameter(
            displayName="maximale afstand vlak kolk",
            name="max_vlak_kolk",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input",
            defaultValue=MAX_AFSTAND_VLAK_KOLK,
        ),
        max_afgekoppeld = parameter(
            displayName="maximale afstand afgekoppeld",
            name="max_afgekoppeld",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input",
            defaultValue=MAX_AFSTAND_AFGEKOPPELD,
        ),
        max_drievoudig = parameter(
            displayName="maximale afstand drievoudig",
            name="max_drievoudig",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input",
            defaultValue=MAX_AFSTAND_DRIEVOUDIG,
        ),
        afkoppelen_daken = parameter(
            displayName="afkoppelen hellende daken",
            name="afkoppelen_daken",
            datatype="GPBoolean",
            parameterType="Required",
            direction="Input",
            defaultValue=AFKOPPELEN_HELLENDE_DAKEN,
        ),
        bouwjaar_riool = parameter(
            displayName="bouwjaar gescheiden binnenhuisriolering",
            name="bouwjaar_riool",
            datatype="GPLong",
            parameterType="Required",
            direction="Input",
            defaultValue=BOUWJAAR_GESCHEIDEN_BINNENHUISRIOLERING,
        ),
        verhardingsgraaf_erf = parameter(
            displayName="verhardingsgraad erf",
            name="verhardingsgraaf_erf",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input",
            defaultValue=VERHARDINGSGRAAD_ERF,
        ),
        verhardingsgraad_half_verhard = parameter(
            displayName="verhardingsgraad half verhard",
            name="verhardingsgraad_half_verhard",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input",
            defaultValue=VERHARDINGSGRAAD_HALF_VERHARD,
        ),
        bgt_oppervlakken_symb = parameter(
            displayName="BGT oppervlakken symbology",
            name="bgt_oppervlakken_symb",
            datatype="GPLayer",
            parameterType="Derived",
            direction="Output",
            symbology=os.path.join(layers, "bgt_oppervlakken.lyrx"),
        ),
        bgt_inlooptabel_symb = parameter(
            displayName="BGT Inlooptabel symoblogy",
            name="bgt_inlooptabel_symb",
            datatype="GPLayer",
            parameterType="Derived",
            direction="Output",
            symbology=os.path.join(layers, "bgt_inlooptabel.lyrx"),
        ),
        gwsw_lijn_symb = parameter(
            displayName="GWSW lijnen symbology",
            name="gwsw_lijn_symb",
            datatype="GPLayer",
            parameterType="Derived",
            direction="Output",
            symbology=os.path.join(layers, "gwsw_lijn.lyrx"),
        ),
        copy_pipe_codes =  parameter(
            displayName="Leidingcodes koppelen",
            name="copy_pipe_codes",
            datatype="GPBoolean",
            parameterType="Required",
            direction="Input",
        )
        copy_pipe_codes.value = False

        return [previous_results, bgt, leidingen, bag, kolken_file, input_extent_mask_wkt, input_statistics_shape, output_gpkg, max_vlak_afwatervoorziening, max_vlak_oppwater,
                                max_pand_opwater, max_vlak_kolk, max_afgekoppeld, max_drievoudig, afkoppelen_daken, bouwjaar_riool, verhardingsgraaf_erf,
                                verhardingsgraad_half_verhard, bgt_oppervlakken_symb, bgt_inlooptabel_symb, gwsw_lijn_symb, copy_pipe_codes]

    def updateParameters(self, parameters):
        """
        updates a parameter in the interface if specified
        """
        output_gpkg = parameters[self.output_gpkg_idx]
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
        bgt_file = parameters[self.bgt_idx]
        pipe_file = parameters[self.leidingen_idx]
        bag_file = parameters[self.bag_idx]
        input_area = parameters[self.input_extent_mask_wkt_idx]

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

            bgt_file = parameters[self.bgt_idx].valueAsText
            pipe_file = parameters[self.leidingen_idx].valueAsText
            building_file = parameters[self.bag_idx].valueAsText
            kolken_file = parameters[self.kolken_file_idx].valueAsText
            input_area = parameters[self.input_extent_mask_wkt_idx].valueAsText
            output_gpkg = parameters[self.output_gpkg_idx].valueAsText
            previous_results_file = parameters[self.previous_results_idx].valueAsText
            statistics_area = parameters[self.input_statistics_shape_idx].valueAsText

            core_parameters = InputParameters(
                max_afstand_vlak_afwateringsvoorziening=parameters[self.max_vlak_afwatervoorziening_idx].value,
                max_afstand_vlak_oppwater=parameters[self.max_vlak_oppwater_idx].value,
                max_afstand_pand_oppwater=parameters[self.max_pand_opwater_idx].value,
                max_afstand_vlak_kolk=parameters[self.max_vlak_kolk_idx].value,
                max_afstand_afgekoppeld=parameters[self.max_afgekoppeld_idx].value,
                max_afstand_drievoudig=parameters[self.max_drievoudig_idx].value,
                afkoppelen_hellende_daken=parameters[self.afkoppelen_daken_idx].value,
                gebruik_bag=building_file != None,
                gebruik_kolken=kolken_file != None,
                gebruik_resultaten=previous_results_file!= None,
                gebruik_statistieken=statistics_area!= None,
                bouwjaar_gescheiden_binnenhuisriolering=parameters[self.bouwjaar_riool_idx].value,
                verhardingsgraad_erf=parameters[self.verhardingsgraaf_erf_idx].value,
                verhardingsgraad_half_verhard=parameters[self.verhardingsgraad_half_verhard_idx].value,
                leidingcodes_koppelen=parameters[self.copy_pipe_codes_idx].value
            )

            # Output layers
            bgt_oppervlakken_symb = parameters[self.bgt_oppervlakken_symb_idx]
            bgt_inlooptabel_symb = parameters[self.bgt_inlooptabel_symb_idx]
            gwsw_lijn_symb = parameters[self.gwsw_lijn_symb_idx]

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
                [bgt_oppervlakken_symb, bgt_inlooptabel_symb, gwsw_lijn_symb], self.bgt_oppervlakken_symb_idx
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
