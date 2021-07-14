import arcpy
import sys
import os


def add_layers_to_map(save_database, arcgis_com):
    # Add layers to map
    try:
        # TODO omschrijven naar nieuwe Visualize class structuur!
        dataset = os.path.join(save_database, 'main.bgt_inlooptabel')
        # temporary, create copy in a gdb, because the right field is not available
        dataset = _layers_to_gdb(save_database, dataset)
        layers = os.path.join(os.path.dirname(__file__), 'layers')

        arcgis_com.AddMessage('You are in ArcGIS Pro')

        # Symbology layer for both ArcMap and ArcGIS Pro
        symbology_layer_path = os.path.join(layers, "inlooptabel_bgt.lyrx")
        arcgis_com.AddMessage('symbology_layer path is {}'.format(symbology_layer_path))

        # Read ArcGIS Pro project and Map
        aprx = arcpy.mp.ArcGISProject("CURRENT")
        map = aprx.listMaps()[0]

        input_layer = map.addDataFromPath(dataset)
        layer_file = arcpy.mp.LayerFile(symbology_layer_path)
        for layer in layer_file.listLayers():
            sym_layer = layer
        arcpy.ApplySymbologyFromLayer_management(input_layer, sym_layer)
        arcpy.SetParameterAsText(16, input_layer)
        # https://support.esri.com/en/bugs/nimbus/QlVHLTAwMDExOTkwNw==
        # workaround works when parameter 16 is defined as a layer and as parameterType Derived
        aprx.save()

    except:
        arcgis_com.Traceback()


if __name__ == '__main__':

    from cls_general_use import GeneralUse
    arcgis_com = GeneralUse(sys, arcpy)
    save_database = r'C:\Users\hsc\OneDrive - Tauw Group bv\ArcGIS\Projects\bgt_inlooptool\mem21.gpkg'
    add_layers_to_map(save_database, arcgis_com)

    print('helemaal klaar!')
