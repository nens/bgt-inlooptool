import arcpy
import sys
import os

python_version = int(str(sys.version)[0])


def add_layers_to_map(save_database, arcgis_com):
    # Add layers to map
    try:
        dataset = os.path.join(save_database, 'main.bgt_inlooptabel')
        # temporary, create copy in a gdb, because the right field is not available
        dataset = _layers_to_gdb(save_database, dataset)
        layers = os.path.join(os.path.dirname(__file__), 'layers')

        # TODO alternate way to check for ArcMap or ArcGIS Pro? als exe?
        if python_version == 2:
            arcgis_com.AddMessage('You are in ArcMap')

            # Symbology layer for both ArcMap and ArcGIS Pro
            symbology_layer_path = os.path.join(layers, "symb_bgt_inlooptabel.lyr")
            arcgis_com.AddMessage('symbology_layer path is {}'.format(symbology_layer_path))

            # Weergeven van resultaten in ArcMap
            mxd = arcpy.mapping.MapDocument('CURRENT')
            df = arcpy.mapping.ListDataFrames(mxd)[0]

            # Add layer with symbology
            add_symbology_layer = arcpy.mapping.Layer(symbology_layer_path)
            add_symbology_layer.replaceDataSource(save_database, "FILEGDB_WORKSPACE", "main_bgt_inlooptabel")
            arcpy.mapping.AddLayer(df, add_symbology_layer)

            mxd.save()

        elif python_version == 3:
            arcgis_com.AddMessage('You are in ArcGIS Pro')

            # Symbology layer for both ArcMap and ArcGIS Pro
            symbology_layer_path = os.path.join(layers, "inlooptabel_bgt.lyrx")
            arcgis_com.AddMessage('symbology_layer path is {}'.format(symbology_layer_path))

            # Read ArcGIS Pro project and Map
            aprx = arcpy.mp.ArcGISProject(r"C:\Users\hsc\OneDrive - Tauw Group bv\ArcGIS\Projects\bgt_inlooptool\bgt_inlooptool.aprx")
            # aprx = arcpy.mp.ArcGISProject("CURRENT")
            map = aprx.listMaps()[0]

            # # TODO if directly from gpkg, eerst moet N&S symbology veld toevoegen in code
            # try:
            #     layer = map.addDataFromPath(dataset)
            #     symbology_layer = arcpy.mp.LayerFile(symbology_layer_path)
            #     arcpy.ApplySymbologyFromLayer_management(layer, symbology_layer)
            #     # TODO als Nelen en Schuurman dit in de core doet aanzetten!
            # except Exception:
            #     arcgis_com.Traceback()

            # If gpkg does not work
            input_layer = map.addDataFromPath(dataset)
            layer_file = arcpy.mp.LayerFile(symbology_layer_path)
            for layer in layer_file.listLayers():
                sym_layer = layer
            arcpy.ApplySymbologyFromLayer_management(input_layer, sym_layer)
            # TODO werkt wel vanuit test.py maar niet vanuit hier!
            # Apply the symbology from the symbology layer to the input layer
            # arcpy.ApplySymbologyFromLayer_management(new_layer, symbology_layer)
            # door bug wordt dit niet goed weergegeven vanuit de tool. fix in ArcGIS Pro 2.7
            # https://support.esri.com/en/bugs/nimbus/QlVHLTAwMDEyMDkwNg==
            aprx.save()

        else:
            arcgis_com.AddMessage('Python version is {} and is not supported'.format(python_version))
    except:
        arcgis_com.Traceback()


def _layers_to_gdb(save_database, dataset):

    try:
        # If gpkg does not work
        save_gdb = save_database.replace('.gpkg', '.gdb')
        if not arcpy.Exists(save_gdb):
            arcpy.CreateFileGDB_management(os.path.dirname(save_gdb), os.path.basename(save_gdb))
        ws = save_gdb
        arcpy.env.workspace = ws
        arcpy.env.overwriteOutput = True
        fc_name = 'main_bgt_inlooptabel'
        out_dataset = str(arcpy.FeatureClassToFeatureClass_conversion(dataset, ws, fc_name))
        _bgt_inloop_symbology(out_dataset)
        # out_dataset = os.path.join(save_database, 'main_bgt_inlooptabel')

        return out_dataset
    except:
        arcgis_com.Traceback()


def _bgt_inloop_symbology(out_dataset):

    # todo checken wat de goede symbology moet zijn!
    try:
        arcpy.AddField_management(out_dataset, 'categorie', 'TEXT', field_length=100)
        field_list = ['hemelwaterriool', 'gemengd_riool', 'open_water', 'maaiveld', 'categorie']
        with arcpy.da.UpdateCursor(out_dataset, field_list) as cursor:
            for row in cursor:
                if row[0] == 100:  # hemelwaterriool = 100
                    categorie = "RWA"
                elif row[1] == 100:  # gemengd riool = 100
                    categorie = "Gemengd"
                elif row[2] == 100 or row[3] == 100:  # niet_aangesloten = 100
                    categorie = "Maaiveld (niet aangesloten op riolering)"
                elif 0 < row[0] < 100 and 0 < row[1] < 100:
                    categorie = "RWA / Gemengd 50-50"
                else:
                    categorie = "Alle andere waarden"
                row[4] = categorie
                cursor.updateRow(row)
    except:
        arcgis_com.Traceback()


if __name__ == '__main__':

    from cls_general_use import GeneralUse
    arcgis_com = GeneralUse(sys, arcpy)
    save_database = r'C:\Users\hsc\OneDrive - Tauw Group bv\ArcGIS\Projects\bgt_inlooptool\mem21.gpkg'
    add_layers_to_map(save_database, arcgis_com)

    print('helemaal klaar!')
