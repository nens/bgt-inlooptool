import arcpy
from bgt_inlooptool.cls_general_use import GeneralUse


class VisualizeLayers:

    def __init__(self, arcgis_project=None):

        if arcgis_project is None:
            self.aprx = arcpy.mp.ArcGISProject("CURRENT")
            self.map = self.aprx.activeMap
        else:
            self.aprx = arcpy.mp.ArcGISProject(arcgis_project)
            self.map = self.aprx.listMaps()[0]
        self.arcgis_com = GeneralUse()

    def save(self):
        self.aprx.save()

    def add_layer_to_map(self, in_dataset, param_nr, symbology_layer=None):
        """
        Add layers to map with symbology if a symbology layer is specified
        """
        try:
            # add data to the map
            output_layer = self.map.addDataFromPath(in_dataset)
            if symbology_layer is not None:
                layer_file = arcpy.mp.LayerFile(symbology_layer)
                for layer in layer_file.listLayers():
                    sym_layer = layer
                    break
                else:  # TODO hier onderzoeken hoe die layer file structuur in elkaar zit!
                    sym_layer = layer_file
                arcpy.ApplySymbologyFromLayer_management(output_layer, sym_layer)
                arcpy.SetParameterAsText(param_nr, output_layer)
                # https://support.esri.com/en/bugs/nimbus/QlVHLTAwMDExOTkwNw==
                # workaround works when parameter 16 is defined as a layer and as parameterType Derived
        except Exception:
            self.arcgis_com.Traceback()
