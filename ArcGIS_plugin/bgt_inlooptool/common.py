import arcpy
import os

SPATIAL_REFERENCE_CODE = 28992  # RD_NEW


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
              enabled=True, multiValue=False):
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
        multiValue=multiValue)

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
