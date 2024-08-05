# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 09:40:20 2024

@author: ruben.vanderzaag
"""

from osgeo import ogr

def _write_to_disk(file_path, db_layer_name, dst_layer_name): 
    """Copy mem_database to file_path"""
    # Get the source layer from the memory database
    db_layer = mem_database.GetLayerByName(db_layer_name)
    if db_layer is None:
        raise ValueError(f"Layer '{db_layer_name}' not found in memory database.")
    
    # Open the destination GeoPackage in write mode
    dst_gpkg = GPKG_DRIVER.Open(file_path, 1)  # 1 means writable
    if dst_gpkg is None:
        raise ValueError(f"Could not open GeoPackage '{file_path}' for writing.")
    
    # Get the destination layer from the GeoPackage
    dst_layer = dst_gpkg.GetLayerByName(dst_layer_name)
    if dst_layer is None:
        raise ValueError(f"Layer '{dst_layer_name}' not found in destination GeoPackage.")
    
    # Get the layer definitions for both the source and destination layers
    layer_defn = db_layer.GetLayerDefn()
    dst_layer_defn = dst_layer.GetLayerDefn()
    
    # Optional: Check if field counts are consistent
    if layer_defn.GetFieldCount() != dst_layer_defn.GetFieldCount():
        print(f"Warning: Source and destination layers have different field counts: {layer_defn.GetFieldCount()} vs {dst_layer_defn.GetFieldCount()}")
    
    # Create a mapping from destination field names to source field indices --> to do: make more efficient (takes much time)
    field_mapping = {}
    for i in range(dst_layer_defn.GetFieldCount()):
        dst_field_name = dst_layer_defn.GetFieldDefn(i).GetName()
        for j in range(layer_defn.GetFieldCount()):
            src_field_name = layer_defn.GetFieldDefn(j).GetName()
            if dst_field_name == src_field_name:
                field_mapping[dst_field_name] = j
                #print(f"{dst_field_name} found")
                break
    
    for feature in db_layer:
        dst_feature = ogr.Feature(dst_layer_defn)
        for dst_field_name, src_field_index in field_mapping.items():
            value = feature.GetField(src_field_index)
            dst_feature.SetField(dst_field_name, value)
    
        # Copy geometry from source feature to destination feature
        geom = feature.GetGeometryRef()
        if geom:
            dst_feature.SetGeometry(geom.Clone())
        else:
            print("No geometry found for feature.")
    
        # Create the feature in the destination layer
        dst_layer.CreateFeature(dst_feature)
    
    """
    for i in range(dst_layer_defn.GetFieldCount()):
        field_name = None
        for j in range(layer_defn.GetFieldCount()):
            if dst_layer_defn.GetFieldDefn(i).GetName()==layer_defn.GetFieldDefn(j).GetName():
                field_name =layer_defn.GetFieldDefn(i).GetName()
                #print(f"{field_name} found")
                break
        if field_name:
            for feature in self.db_layer:
                dst_feature = ogr.Feature(dst_layer_defn)
                dst_feature.SetField(field_name, feature.GetField(i))
        else:
            print(f"Field {dst_layer_defn.GetFieldDefn(i).GetName()} not found!")
    
    """
    """
    # Iterate through each feature in the source layer
    for feature in self.db_layer:
        dst_feature = ogr.Feature(dst_layer_defn)
        for i in range(dst_layer_defn.GetFieldCount()):
            field_name = None
            for j in range(layer_defn.GetFieldCount()):
                if dst_layer_defn.GetFieldDefn(i).GetName()==layer_defn.GetFieldDefn(j).GetName():
                    field_name =layer_defn.GetFieldDefn(i).GetName()
                    print(f"{field_name} found")
                    break
            if field_name:
                dst_feature.SetField(field_name, feature.GetField(i))
            else:
                print("Field not found!")
        
        # Copy geometry from source feature to destination feature
        geom = feature.GetGeometryRef()
        if geom:
            dst_feature.SetGeometry(geom.Clone())
        else:
            print("No geometry found for feature.")
        
        # Create the feature in the destination layer
        self.dst_layer.CreateFeature(dst_feature)
        """
    # Clean up
    dst_gpkg = None
    dst_layer = None
    feature = None
    db_layer = None
    print("Done with saving")


from osgeo import ogr

# Path to the GeoPackage file
gpkg_path = r"C:\Users\ruben.vanderzaag\Documents\Github\bgt-inlooptool\QGIS_plugin\bgtinlooptool\style\output_bgtinlooptool_v2.gpkg"

# Open the GeoPackage
data_source = ogr.Open(gpkg_path, 0)  # 0 means read-only, 1 means writeable

if data_source is None:
    print("Failed to open the GeoPackage.")
else:
    # Get the layer by name or index (0-based index)
    layer_name = "bgt_inlooptabel"  # replace with the actual layer name
    layer = data_source.GetLayerByName(layer_name)
    # Alternatively, you can use: layer = data_source.GetLayerByIndex(0)

    if layer is None:
        print(f"Layer '{layer_name}' not found.")
    else:
        print(f"Layer '{layer_name}' opened successfully.")

        # Create an in-memory data source
        MEM_DRIVER = ogr.GetDriverByName("Memory")
        mem_database = MEM_DRIVER.CreateDataSource("")

        # Get the layer's schema (definition)
        layer_defn = layer.GetLayerDefn()

        # Create the in-memory layer with the same schema
        mem_layer = mem_database.CreateLayer(layer_name, layer.GetSpatialRef(), layer_defn.GetGeomType())

        # Copy fields from the source layer to the in-memory layer
        for i in range(layer_defn.GetFieldCount()):
            field_defn = layer_defn.GetFieldDefn(i)
            mem_layer.CreateField(field_defn)

        # Get the definition of the in-memory layer (to be used for creating features)
        mem_layer_defn = mem_layer.GetLayerDefn()

        # Copy features from the source layer to the in-memory layer
        for feature in layer:
            # Create a new feature for the in-memory layer
            mem_feature = ogr.Feature(mem_layer_defn)
            
            # Set feature attributes
            for i in range(mem_layer_defn.GetFieldCount()):
                mem_feature.SetField(mem_layer_defn.GetFieldDefn(i).GetNameRef(), feature.GetField(i))

            # Set feature geometry
            geom = feature.GetGeometryRef()
            if geom:
                mem_feature.SetGeometry(geom.Clone())

            # Add the feature to the in-memory layer
            mem_layer.CreateFeature(mem_feature)

            # Destroy the in-memory feature to free resources
            mem_feature = None

        # The in-memory layer is now ready for use
        print(f"Layer '{layer_name}' copied to in-memory database.")

    # Clean up
    data_source = None
    mem_database = None
