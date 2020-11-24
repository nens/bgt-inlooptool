import arcpy
import sys
import os

python_version = str(sys.version)[0]

# Add layers to map
def add_layers_to_map(save_database):

    # TODO alternate way to check for ArcMap or ArcGIS Pro? als exe?
    if python_version == 2:
        print('You are in ArcMap')

        # Weergeven van resultaten in ArcMap
        try:
            mxd = arcpy.mapping.MapDocument('CURRENT')
        except:
            mxd = None
            arcpy.AddMessage('Niet in ArcMap')
        if not mxd is None:
            arcpy.AddMessage('In ArcMap')
            df = arcpy.mapping.ListDataFrames(mxd)[0]
            layer_dir = os.path.join(os.path.dirname(__file__), "Layers")

            # Add Layer
            add_layer1 = arcpy.mapping.Layer("uitlaat_vlak")
            arcpy.mapping.AddLayer(df, add_layer1, "AUTO_ARRANGE")

            # Add layer with symbology
            add_symbology_layer = arcpy.mapping.Layer(os.path.join(layer_dir, 'test.lyr'))
            add_symbology_layer.replaceDataSource(save_database, "FILEGDB_WORKSPACE", "test")
            arcpy.mapping.AddLayer(df, add_symbology_layer)


    elif python_version == 3:
        print('You are in ArcGIS Pro')

        # Read ArcGIS Pro project and Map
        aprx = arcpy.mp.ArcGISProject("CURRENT")
        map = aprx.listMaps()[0]

        arcpy.env.workspace = save_database
        layer_list = arcpy.ListFeatureClasses()  # Also works on gpkg

        for layer in layer_list:
            dataset = os.path.join(save_database, layer)
            map.addDataFromPath(dataset)