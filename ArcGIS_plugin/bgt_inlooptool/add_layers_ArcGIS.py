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

def layers_to_gdb(input_geopackage, output_gdb):

    # TODO bepalen of we alleen een nieuwe gdb doen of niet?
    arcpy.CreateFileGDB_management(os.path.dirname(output_gdb), os.path.basename(output_gdb))

    arcpy.env.workspace = input_geopackage
    layer_list = arcpy.ListFeatureClasses()
    for layer in layer_list:
        desc_layer = arcpy.Describe(layer)
        layername = str(layer[5:])
        print(layername)
        arcpy.FeatureClassToFeatureClass_conversion(layer, output_gdb, layername)
        print('wait!')


    print('Klaar!')

if __name__ == '__main__':

    temp = arcpy.GetSystemEnvironment("TEMP")
    gpkg_path = os.path.join(temp, 'bgt_inlooptool.gpkg')
    input_geopackage = r'C:\GIS\test3.gpkg'
    output_gdb = r'C:\GIS\output3.gdb'
    layers_to_gdb(input_geopackage, output_gdb)

    print('helemaal klaar!')