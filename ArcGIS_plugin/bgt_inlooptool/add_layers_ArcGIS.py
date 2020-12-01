import arcpy
import sys
import os

from cls_General_use import GeneralUse
arcgis_com = GeneralUse(sys, arcpy)

python_version = str(sys.version)[0]

# Add layers to map
def add_layers_to_map(save_database):

    # Symbology layer for both ArcMap and ArcGIS Pro
    layers = os.path.join(os.path.dirname(__file__), 'layers')
    symbology_layer = "bgt_inlooptabel.lyr"

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

            # gpkg layer toevoegen in ArcMap lijkt niet te werken via Python
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

        dataset = os.path.join(save_database, 'main.bgt_inlooptabel')
        # TODO if directly from gpkg werkend maken!
        try:
            layer = map.addDataFromPath(dataset)
        except Exception:
            arcgis_com.Traceback()

        # If gpkg does not work
        out_dataset = layers_to_gdb(save_database, dataset)
        layer = map.addDataFromPath(out_dataset)

        # Apply the symbology from the symbology layer to the input layer
        arcpy.ApplySymbologyFromLayer_management(layer, symbology_layer)


def layers_to_gdb(save_database, dataset):

    # If gpkg does not work
    save_gdb = save_database.replace('.gpkg', '.gdb')
    if not arcpy.Exists(save_gdb):
        ws = arcpy.CreateFileGDB_management(os.path.dirname(save_gdb), os.path.basename((save_gdb)))
    arcpy.env.workspace = ws
    fc_name = 'main_bgt_inlooptabel'
    arcpy.FeatureClassToGeodatabase_conversion(dataset, fc_name)
    out_dataset = os.path.join(save_database, 'main_bgt_inlooptabel')

    return out_dataset

def bgt_inloop_symbology(out_dataset):

    arcpy.AddField_management(out_dataset, 'categorie', 'TEXT', field_length=100)
    field_list = ['hemelwaterriool', 'gemengd_riool', 'niet_aangesloten', 'categorie']
    with arcpy.da.UpdateCursor(out_dataset, field_list) as cursor:
        for row in cursor:
            if row[0] == 100:  # hemelwaterriool = 100
                categorie = "RWA"
            elif row[1] == 100:  # gemengd riool = 100
                categorie = "Gemengd"
            elif row[2] == 100:  # niet_aangesloten = 100
                categorie = "Maaiveld (niet aangesloten op riolering)"
            elif 0 < row[0] < 100 and 0 < row[1] < 100:
                categorie = "RWA / Gemengd 50-50"
            else:
                categorie = "Alle andere waarden"
            row[3] = categorie
            cursor.updateRow(row)


if __name__ == '__main__':

    temp = arcpy.GetSystemEnvironment("TEMP")
    gpkg_path = os.path.join(temp, 'bgt_inlooptool.gpkg')
    input_geopackage = r'C:\GIS\test3.gpkg'
    output_gdb = r'C:\GIS\output3.gdb'
    layers_to_gdb(input_geopackage, output_gdb)

    print('helemaal klaar!')