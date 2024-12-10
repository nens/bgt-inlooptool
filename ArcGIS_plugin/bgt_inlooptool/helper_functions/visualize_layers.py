import arcpy
from .cls_general_use import GeneralUse
from typing import Union
from .constants import VisualizeLayer


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

    def add_layer_to_map(
        self, visualize_settings: VisualizeLayer, 
    ):
        """
        Add layers to map with symbology if a symbology layer is specified
        """
        try:
            # add data to the map
            output_layer = self.map.addDataFromPath(visualize_settings.symbology_param.valueAsText)
            output_layer.name = visualize_settings.layer_name
            return output_layer
        except Exception:
            self.arcgis_com.Traceback()


    def apply_symbology(self, visualize_settings: VisualizeLayer, added_layer):
            
        try:
            # add symbology if it is available
            layer_file = arcpy.mp.LayerFile(visualize_settings.symbology_param.symbology)
            for layer in layer_file.listLayers():
                sym_layer = layer
                break
            else:
                sym_layer = layer_file
            arcpy.ApplySymbologyFromLayer_management(added_layer, sym_layer)
            arcpy.SetParameterAsText(visualize_settings.params_idx, added_layer)
            # https://support.esri.com/en/bugs/nimbus/QlVHLTAwMDExOTkwNw==
            # workaround works when parameter 16 is defined as a layer and as parameterType Derived

        except Exception:
            self.arcgis_com.Traceback()

