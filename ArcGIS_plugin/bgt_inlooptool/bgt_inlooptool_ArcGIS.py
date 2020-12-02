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
from add_layers_ArcGIS import add_layers_to_map

# import bgt inlooptool
# TODO voor arcmap mogelijk zonder core.
from core.inlooptool import InloopTool, InputParameters, Database
from core.defaults import (MAX_AFSTAND_VLAK_AFWATERINGSVOORZIENING,
                           MAX_AFSTAND_VLAK_OPPWATER,
                           MAX_AFSTAND_PAND_OPPWATER,
                           MAX_AFSTAND_VLAK_KOLK,
                           MAX_AFSTAND_AFGEKOPPELD,
                           MAX_AFSTAND_DRIEVOUDIG,
                           AFKOPPELEN_HELLENDE_DAKEN,
                           BOUWJAAR_GESCHEIDEN_BINNENHUISRIOLERING,
                           VERHARDINGSGRAAD_ERF,
                           VERHARDINGSGRAAD_HALF_VERHARD)


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
            parameter(displayName='BAG (als geopackage)',
                      name='bag',
                      datatype="DEDatasetType",
                      parameterType="Optional",
                      direction="Input",
                      defaultValue=r"C:\GIS\test_data_inlooptool\bag.gpkg"),
            parameter(displayName='BGT (als zipfile)',
                      name='bgt',
                      datatype="DEFile",
                      parameterType="Required",
                      direction="Input",
                      defaultValue=r"C:\GIS\test_data_inlooptool\extract.zip"),
            parameter(displayName='Leidingen (als geopackage)',
                      name='leidingen',
                      datatype='DEDatasetType',
                      parameterType='Required',
                      direction='Input',
                      defaultValue=r"C:\GIS\test_data_inlooptool\getGeoPackage_1134.gpkg"),
            parameter(displayName='Opslag locatie gdb',
                      name='output_gpkg',
                      datatype='DEDatasetType',
                      # parameterType='Required',
                      # direction='Output'),
                      defaultValue=r"C:\Users\hsc\OneDrive - Tauw Group bv\ArcGIS\Projects\bgt_inlooptool\mem_database.gpkg"),
            parameter(displayName='maximale afstand vlak afwateringsvoorziening',
                      name='max_vlak_afwatervoorziening',
                      datatype='GPDouble',
                      parameterType='Required',
                      direction='Input',
                      defaultValue=MAX_AFSTAND_VLAK_AFWATERINGSVOORZIENING),
            parameter(displayName='maximale afstand vlak oppervlaktewater',
                      name='max_vlak_oppwater',
                      datatype='GPDouble',
                      parameterType='Required',
                      direction='Input',
                      defaultValue=MAX_AFSTAND_VLAK_OPPWATER),
            parameter(displayName='maximale afstand pand oppervlaktewater',
                      name='max_pand_opwater',
                      datatype='GPDouble',
                      parameterType='Required',
                      direction='Input',
                      defaultValue=MAX_AFSTAND_PAND_OPPWATER),
            parameter(displayName='maximale afstand vlak kolk',
                      name='max_vlak_kolk',
                      datatype='GPDouble',
                      parameterType='Required',
                      direction='Input',
                      defaultValue=MAX_AFSTAND_VLAK_KOLK),
            parameter(displayName='maximale afstand afgekoppeld',
                      name='max_afgekoppeld',
                      datatype='GPDouble',
                      parameterType='Required',
                      direction='Input',
                      defaultValue=MAX_AFSTAND_AFGEKOPPELD),
            parameter(displayName='maximale afstand drievoudig',
                      name='max_drievoudig',
                      datatype='GPDouble',
                      parameterType='Required',
                      direction='Input',
                      defaultValue=MAX_AFSTAND_DRIEVOUDIG),
            parameter(displayName='afkoppelen hellende daken',
                      name='afkoppelen_daken',
                      datatype='GPBoolean',
                      parameterType='Required',
                      direction='Input',
                      defaultValue=AFKOPPELEN_HELLENDE_DAKEN),
            parameter(displayName='bouwjaar gescheiden binnenhuisriolering',
                      name='bouwjaar_riool',
                      datatype='GPLong',
                      parameterType='Required',
                      direction='Input',
                      defaultValue=BOUWJAAR_GESCHEIDEN_BINNENHUISRIOLERING),
            parameter(displayName='verhardingsgraad erf',
                      name='verhardingsgraaf_erf',
                      datatype='GPDouble',
                      parameterType='Required',
                      direction='Input',
                      defaultValue=VERHARDINGSGRAAD_ERF),
            parameter(displayName='verhardingsgraad half verhard',
                      name='verhardingsgraad_half_verhard',
                      datatype='GPDouble',
                      parameterType='Required',
                      direction='Input',
                      defaultValue=VERHARDINGSGRAAD_HALF_VERHARD)
            ]

        return self.parameters

    def updateParameters(self, parameters):

        if parameters[3].value == True:
            parameters[4].enabled = True  # Enable the output gdb
        else:
            parameters[4].enabled = False  # Disable the output gdb

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
            self.arcgis_com = GeneralUse(sys, arcpy)
            self.arcgis_com.StartAnalyse()
            self.arcgis_com.AddMessage("Start BGT Inlooptool!")

            building_file = parameters[0].valueAsText
            bgt_file = parameters[1].valueAsText
            pipe_file = parameters[2].valueAsText
            output_gpkg = parameters[3].valueAsText

            core_parameters = InputParameters(
                max_afstand_vlak_afwateringsvoorziening=parameters[4].value,
                max_afstand_vlak_oppwater=parameters[5].value,
                max_afstand_pand_oppwater=parameters[6].value,
                max_afstand_vlak_kolk=parameters[7].value,
                max_afstand_afgekoppeld=parameters[8].value,
                max_afstand_drievoudig=parameters[9].value,
                afkoppelen_hellende_daken=parameters[10].value,
                bouwjaar_gescheiden_binnenhuisriolering=parameters[11].value,
                verhardingsgraad_erf=parameters[12].value,
                verhardingsgraad_half_verhard=parameters[13].value)

            # self.it = InloopTool(core_parameters)
            #
            # # Import surfaces and pipes
            # self.arcgis_com.AddMessage("Importing BGT files")
            # self.it.import_surfaces(bgt_file)
            # self.arcgis_com.AddMessage("Importing pipe files")
            # self.it.import_pipes(pipe_file)
            # self.arcgis_com.AddMessage("Importing building files")
            # self.it.import_buildings(building_file)
            # self.it._database.add_build_year_to_surface()  # use_index=self.use_index)
            # self.arcgis_com.AddMessage("Calculating distances")
            # self.it.calculate_distances(parameters=core_parameters) #, use_index=self.use_index)
            # self.arcgis_com.AddMessage("Calculating Runoff targets")
            # self.it.calculate_runoff_targets()
            #
            # # Export results
            # self.arcgis_com.AddMessage("Exporting to GPKG")
            # self.it._database._write_to_disk(output_gpkg)

            # import ogr
            # GPKG_DRIVER = ogr.GetDriverByName("GPKG")
            # GPKG_DRIVER.CopyDataSource(self.it._database.mem_database, database_fn)
            # TODO schrijven naar gdb werkend maken!
            # self.arcgis_com.AddMessage("Exporting to GDB")
            # onderstaande lijkt niet te werken
            # import ogr
            # output_gdb = r'C:\GIS\output.gdb'
            # gdb_driver = ogr.GetDriverByName("OpenFileGDB")
            # gdb_driver.CopyDataSource(self.it._database.mem_database, output_gdb)
            # http://pcjericks.github.io/py-gdalogr-cookbook/layers.html#filter-and-select-input-shapefile-to-new-output-shapefile-like-ogr2ogr-cli
            # https://www.esri.com/arcgis-blog/products/product/data-management/how-to-use-ogc-geopackages-in-arcgis-pro/
            # ogr_lyr = self.it._database.mem_database.GetLayerByName('bgt_inlooptabel')
            # Add layers to the map
            # TODO werkend maken van add_layers_to_map

            self.arcgis_com.AddMessage("Visualiseren van resultaten BGT Inlooptool!")
            add_layers_to_map(output_gpkg, self.arcgis_com)


        except Exception:
            self.arcgis_com.Traceback()
        finally:
            self.arcgis_com.AddMessage("Klaar")
        return


if __name__ == '__main__':
    # This is used for debugging. Using this separated structure makes it much
    # easier to debug using standard Python development tools.

    try:
        tool = BGTInloopToolArcGIS()
        params = tool.getParameterInfo()

        # bag_file
        params[0].value = r"C:\GIS\test_data_inlooptool\bag.gpkg"
        # bgt_file
        params[1].value = r"C:\GIS\test_data_inlooptool\extract.zip"
        # pipe_file
        params[2].value = r"C:\GIS\test_data_inlooptool\getGeoPackage_1134.gpkg"

        # output_location
        params[3].value = r"C:\GIS\bgt_inlooptool2.gpkg"

        # maximale afstand vlak afwateringsvoorziening
        params[4].value = 40
        # maximale afstand vlak oppervlaktewater
        params[5].value = 2
        # maximale afstand pand oppervlaktewater
        params[6].value = 6
        # 'maximale afstand vlak kolk
        params[7].value = 30
        # maximale afstand afgekoppeld
        params[8].value = 3
        # maximale afstand drievoudig
        params[9].value = 4
        # afkoppelen hellende daken
        params[10].value = True
        # bouwjaar gescheiden binnenhuisriolering
        params[11].value = 1992
        # verhardingsgraad erf
        params[12].value = 50
        # verhardingsgraad half verhard
        params[13].value = 50

        tool.execute(parameters=params, messages=None)

    except Exception as ex:
        print('iets ging fout!')
