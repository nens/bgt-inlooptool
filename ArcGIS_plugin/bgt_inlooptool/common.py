import arcpy
import os
import sys
import json
from cls_general_use import GeneralUse
from collections import namedtuple
arcgis_com = GeneralUse(sys, arcpy)

SPATIAL_REFERENCE_CODE = 28992  # RD_NEW


def layers_to_gdb(input_dataset, output_gdb):
    """
    Converts the gpkg features to a feature class in a gdb
    """
    try:
        if not arcpy.Exists(output_gdb):
            arcpy.CreateFileGDB_management(os.path.dirname(output_gdb), os.path.basename(output_gdb))
        arcpy.env.workspace = output_gdb
        arcpy.env.overwriteOutput = True

        fc_name = os.path.basename(input_dataset).replace('.', '_')
        out_dataset = str(arcpy.FeatureClassToFeatureClass_conversion(input_dataset, output_gdb, fc_name))

        return out_dataset
    except Exception:
        arcgis_com.Traceback()


def add_bgt_inlooptabel_symbologyfield(out_dataset):
    """
    Maakt een categorie veld aan waarop de output symbology voor de BGTInlooptool op gebaseerd is.
    Dit is gemaakt zoals de QML styles voor de QGIS plugin
    """
    try:
        arcpy.AddField_management(out_dataset, 'categorie', 'TEXT', field_length=100)
        field_list = ['hemelwaterriool', 'vgs_hemelwaterriool', 'gemengd_riool', 'vuilwaterriool',
                      'infiltratievoorziening', 'open_water', 'maaiveld', 'categorie']
        field_tuple = namedtuple('field_tuple', field_list)
        with arcpy.da.UpdateCursor(out_dataset, field_list) as cursor:
            for row in cursor:
                data = field_tuple._make(row)
                total_percentage = sum(row[:-1])
                if total_percentage != 100:
                    categorie = "Overig (niet valide, totaal ≠ 100)"
                elif data.hemelwaterriool == 100:  # hemelwaterriool = 100
                    categorie = "Hemelwaterriool 100%"
                elif data.vgs_hemelwaterriool == 100:
                    categorie = "VGS Hemelwaterriool 100%"
                elif data.gemengd_riool == 100:
                    categorie = "Gemengd 100%"
                elif 0 < data.hemelwaterriool < 100 and 0 < data.gemengd_riool < 100:
                    categorie = "Hemelwaterriool en Gemengd"
                elif data.infiltratievoorziening == 100:
                    categorie = "Infiltratievoorziening 100%"
                elif data.maaiveld == 100:
                    categorie = "Maaiveld 100%"
                elif data.open_water == 100:
                    categorie = "Open water 100%"
                else:
                    categorie = "Overig (wel valide, totaal = 100)"
                row[7] = categorie
                cursor.updateRow(row)
    except Exception:
        arcgis_com.Traceback()


def add_gwsw_symbologyfield(out_dataset):
    """
    Maakt een categorie veld aan waarop de output symbology voor de GWSW is gebaseerd!
    """
    try:
        gwsw_json = os.path.join(os.path.dirname(__file__), 'gwsw_lijn.json')
        with open(gwsw_json, 'r') as config_file:
            gwsw_translation = json.load(config_file)

        arcpy.AddField_management(out_dataset, 'type_kort', 'TEXT', field_length=100)
        field_list = ['type', 'type_kort']
        field_tuple = namedtuple('field_tuple', field_list)
        with arcpy.da.UpdateCursor(out_dataset, field_list) as cursor:
            for row in cursor:
                data = field_tuple._make(row)
                type_temp = data.type.split('/')[-1]
                if type_temp in gwsw_translation:
                    type_kort = gwsw_translation[type_temp]
                else:
                    type_kort = "Default (overig)"
                row[1] = type_kort
                cursor.updateRow(row)

    except Exception:
        arcgis_com.Traceback()


def get_wkt_extent(input_fc):
    """
    if the spatial reference is not RD then create a new fc or shapefile next to the existing fc
    """
    arcpy.env.overwriteOutput = True
    arcpy.env.outputZFlag = 'Disabled'  # disables the Z value to make sure we get a WKT extent without Z value

    dir_name = os.path.dirname(input_fc)
    fc_name = os.path.basename(input_fc)
    if fc_name[-4:] == '.shp':
        new_fc_name = f"{fc_name[:-4]}_rd.shp"
    else:
        new_fc_name = f"{fc_name}_rd"

    desc_fc = arcpy.Describe(input_fc)
    spatial_reference_code = desc_fc.SpatialReference.factoryCode
    if spatial_reference_code != SPATIAL_REFERENCE_CODE:
        # if the spatial reference if not set to RD New
        input_fc = arcpy.Project_management(in_dataset=input_fc,
                                            out_dataset=os.path.join(dir_name, new_fc_name),
                                            out_coor_system=arcpy.SpatialReference(SPATIAL_REFERENCE_CODE))

    has_z_value = desc_fc.hasZ
    if has_z_value:  # extent omzetten naar POLYGON en niet naar MULTIPOLYGON Z!
        input_fc = arcpy.FeatureClassToFeatureClass_conversion(input_fc, dir_name, new_fc_name)

    with arcpy.da.SearchCursor(input_fc, ['Shape@WKT']) as cursor:
        for x, row in enumerate(cursor, 1):
            if x == 1:
                input_extent_mask_wkt = row[0]

    if x > 1:
        arcpy.AddWarning("Let op in de input area zitten meerdere features! Alleen de eerste wordt meegenomen!")

    return input_extent_mask_wkt


def parameter(displayName, name, datatype, defaultValue=None, parameterType='Required', direction='Input',
              enabled=True, multiValue=False, symbology=None):
    """
    The parameter implementation makes it a little difficult to quickly
    create parameters with defaults. This method prepopulates the paramaeterType
    and direction parameters and leaves the setting a default value for the
    newly created parameter as optional. The displayName, name and datatype are
    the only required inputs.
    """
    # create parameter with a few defaults
    import arcpy
    param = arcpy.Parameter(
        displayName=displayName,
        name=name,
        datatype=datatype,
        parameterType=parameterType,
        direction=direction,
        enabled=enabled,
        multiValue=multiValue,
        symbology=symbology)

    # set new parameter to a default value
    param.value = defaultValue

    # return the complete parameter object
    return param


class BaseTool(object):
    """
    BaseTool is a custom parent class from which other 'tools' can inherit
    properties and methods.

    The result is fewer lines of code when creating tools that inherit from
    BaseTool. For example, it is not always necessary to override the
    'isLicensed', 'updateParameters', and 'updateMessages' methods.

    """
    __parameters = {}

    def __init__(self):
        """
        Initialization.

        """
        super(BaseTool, self).__init__()
        self.label = ''
        self.description = ''
        self.canRunInBackground = False

    def getParameterInfo(self):
        """
        Define parameter definitions.

        """
        return []

    def isLicensed(self):
        """
        Set whether tool is licensed to execute.

        """
        return True

    def updateParameters(self, parameters):
        """
        Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed.

        """
        for param in parameters:
            self.__parameters[param.name] = param

    def updateMessages(self, parameters):
        """
        Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation.

        """
        pass

    def execute(self, parameters, messages):
        """
        The source code of the tool.

        """
        pass


if __name__ == '__main__':

    # ws = r'C:\Users\hsc\OneDrive - Tauw Group bv\ArcGIS\Projects\bgt_inlooptool\hollands_kroon\bgt_inlooptabel.gpkg'
    # dataset = r'C:\Users\hsc\OneDrive - Tauw Group bv\ArcGIS\Projects\bgt_inlooptool\hollands_kroon\bgt_inlooptabel.gpkg\main.bgt_inlooptabel'

    in_dataset = r'C:\Users\hsc\OneDrive - Tauw Group bv\ArcGIS\Projects\bgt_inlooptool\hollands_kroon\getGeoPackage_2318.gpkg\main.default_lijn'
    out_gdb = r'C:\Users\hsc\OneDrive - Tauw Group bv\ArcGIS\Projects\bgt_inlooptool\hollands_kroon\bgt_inlooptabel.gdb'

    gdb_dataset = layers_to_gdb(input_dataset=in_dataset,
                                output_gdb=out_gdb)
    add_gwsw_symbologyfield(gdb_dataset)
    print('klaar!')
