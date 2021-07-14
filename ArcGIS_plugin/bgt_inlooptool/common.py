import arcpy
import os

SPATIAL_REFERENCE_CODE = 28992  # RD_NEW


def get_wkt_extent(input_fc):
    """
    if the spatial reference is not RD then create a new fc or shapefile next to the existing fc
    """
    if input_fc is not None:
        spatial_reference_code = arcpy.Describe(input_fc).SpatialReference.factoryCode
        if spatial_reference_code != SPATIAL_REFERENCE_CODE:
            dir_name = os.path.dirname(input_fc)
            fc_name = os.path.basename(input_fc)
            if fc_name[-4:] == '.shp':
                new_fc_name = f"{fc_name[-4:]}_rd.shp"
            else:
                new_fc_name = f"{fc_name[-4:]}_rd"
            area_fc = arcpy.Project_management(in_dataset=input_fc,
                                               out_dataset=os.path.join(dir_name, new_fc_name),
                                               out_coor_system=arcpy.SpatialReference(SPATIAL_REFERENCE_CODE))
        else:
            area_fc = input_fc
        with arcpy.da.SearchCursor(area_fc, ['Shape@WKT']) as cursor:
            for row in cursor:
                input_extent_mask_wkt = row[0]

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
