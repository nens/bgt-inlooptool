# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 11:19:23 2024

@author: ruben.vanderzaag
"""

from osgeo import ogr

# Path to the GeoPackage file
gpkg_path = r"C:\Users\ruben.vanderzaag\Documents\Github\bgt-inlooptool\QGIS_plugin\bgtinlooptool\style\template_output5.gpkg"

# Open the GeoPackage
ds = ogr.Open(gpkg_path, update=True)
if ds is None:
    print("Failed to open the GeoPackage.")
    exit(1)

# SQL statement to create the trigger
sql = """
CREATE TRIGGER "trigger_insert_feature_count_4. BGT inlooptabel" AFTER INSERT ON "4. BGT inlooptabel" BEGIN UPDATE gpkg_ogr_contents SET feature_count = feature_count + 1 WHERE lower(table_name) = lower('4. BGT inlooptabel'); END 
"""

# Execute the SQL statement
ds.ExecuteSQL(sql)

# SQL statement to create the trigger
sql = """
CREATE TRIGGER "trigger_delete_feature_count_4. BGT inlooptabel" AFTER DELETE ON "4. BGT inlooptabel" BEGIN UPDATE gpkg_ogr_contents SET feature_count = feature_count - 1 WHERE lower(table_name) = lower('4. BGT inlooptabel'); END 
"""

# Execute the SQL statement
ds.ExecuteSQL(sql)

# Close the data source
ds = None

print("Trigger created successfully.")


# SQL statement to create the trigger
sql = """
CREATE TRIGGER "trigger_insert_feature_count_5. BGT oppervlakken" AFTER INSERT ON "5. BGT oppervlakken" BEGIN UPDATE gpkg_ogr_contents SET feature_count = feature_count + 1 WHERE lower(table_name) = lower('5. BGT oppervlakken'); END 
"""

# Execute the SQL statement
ds.ExecuteSQL(sql)

# SQL statement to create the trigger
sql = """
CREATE TRIGGER "trigger_delete_feature_count_5. BGT oppervlakken" AFTER DELETE ON "5. BGT oppervlakken" BEGIN UPDATE gpkg_ogr_contents SET feature_count = feature_count - 1 WHERE lower(table_name) = lower('5. BGT oppervlakken'); END 
"""

# Execute the SQL statement
ds.ExecuteSQL(sql)

# Close the data source
ds = None

print("Trigger created successfully.")


# SQL statement to create the trigger
sql = """
CREATE TRIGGER "trigger_insert_feature_count_7. Rekeninstellingen" AFTER INSERT ON "7. Rekeninstellingen" BEGIN UPDATE gpkg_ogr_contents SET feature_count = feature_count + 1 WHERE lower(table_name) = lower('7. Rekeninstellingen'); END 
"""

# Execute the SQL statement
ds.ExecuteSQL(sql)

# SQL statement to create the trigger
sql = """
CREATE TRIGGER "trigger_delete_feature_count_7. Rekeninstellingen" AFTER DELETE ON "7. Rekeninstellingen" BEGIN UPDATE gpkg_ogr_contents SET feature_count = feature_count - 1 WHERE lower(table_name) = lower('7. Rekeninstellingen'); END 
"""

# Execute the SQL statement
ds.ExecuteSQL(sql)

# Close the data source
ds = None

print("Trigger created successfully.")

