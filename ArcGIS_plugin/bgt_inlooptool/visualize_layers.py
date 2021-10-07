import arcpy
from cls_general_use import GeneralUse


class VisualizeLayers:

    def __init__(self, arcgis_project=None) -> None:

        if arcgis_project is None:
            self.arcgis_project = arcpy.mp.ArcGISProject("CURRENT")
            self.map = self.arcgis_project.activeMap
        else:
            self.arcgis_project = arcpy.mp.ArcGISProject(arcgis_project)
            self.map = self.arcgis_project.listMaps()[0]

        self.arcgis_com = GeneralUse()

    def save(self):
        self.arcgis_project.save()

    def add_layer_to_map(self, in_param, in_dataset=None, param_nr=None, symbology_layer=None):
        """
        Add layers to map with symbology if a symbology layer is specified
        """
        try:
            # add data to the map
            output_layer = self.map.addDataFromPath(in_param.valueAsText)

            # add symbology if it is available
            if in_param.symbology is not None:
                layer_file = arcpy.mp.LayerFile(in_param.symbology)
                for layer in layer_file.listLayers():
                    sym_layer = layer
                    break
                else:
                    sym_layer = layer_file
                output_layer.name = sym_layer.name
                arcpy.ApplySymbologyFromLayer_management(output_layer, sym_layer)
                arcpy.SetParameterAsText(param_nr, output_layer)
            # https://support.esri.com/en/bugs/nimbus/QlVHLTAwMDExOTkwNw==
            # workaround works when parameter 16 is defined as a layer and as parameterType Derived
        except Exception:
            self.arcgis_com.Traceback()
