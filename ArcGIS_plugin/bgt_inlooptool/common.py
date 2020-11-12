"""
Common things that can be used elsewhere.
"""


def parameter(displayName, name, datatype, defaultValue=None, parameterType='Required', direction='Input',
              enabled=True, multiValue=False):
    '''
    The parameter implementation makes it a little difficult to quickly
    create parameters with defaults. This method prepopulates the paramaeterType
    and direction parameters and leaves the setting a default value for the
    newly created parameter as optional. The displayName, name and datatype are
    the only required inputs.
    '''
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


if __name__ == '__main__':
    pass