"""
@author: Emile.deBadts
"""

SURFACE_TYPE_PAND = "pand"
SURFACE_TYPE_WEGDEEL = "wegdeel"
SURFACE_TYPE_ONDERSTEUNENDWEGDEEL = "ondersteunendwegdeel"
SURFACE_TYPE_BEGROEIDTERREINDEEL = "begroeidterreindeel"
SURFACE_TYPE_ONBEGROEIDTERREINDEEL = "onbegroeidterreindeel"
SURFACE_TYPE_WATERDEEL = "waterdeel"
SURFACE_TYPE_ONDERSTEUNENDWATERDEEL = "ondersteunendwaterdeel"
SURFACE_TYPE_OVERIGBOUWWERK = "overigbouwwerk"
SURFACE_TYPE_GEBOUWINSTALLATIE = "gebouwinstallatie"
SURFACE_TYPE_OVERBRUGGINGSDEEL = "overbruggingsdeel"

ALL_USED_SURFACE_TYPES = {
    SURFACE_TYPE_PAND,
    SURFACE_TYPE_WEGDEEL,
    SURFACE_TYPE_ONDERSTEUNENDWEGDEEL,
    SURFACE_TYPE_BEGROEIDTERREINDEEL,
    SURFACE_TYPE_ONBEGROEIDTERREINDEEL,
    SURFACE_TYPE_WATERDEEL,
    SURFACE_TYPE_ONDERSTEUNENDWATERDEEL,
    SURFACE_TYPE_OVERIGBOUWWERK,
    SURFACE_TYPE_GEBOUWINSTALLATIE,
    SURFACE_TYPE_OVERBRUGGINGSDEEL,
}

from .constants import NOT_FOUND_GEMEENTES, BGT_API_URL, BAG_API_URL, CBS_GEMEENTES_API_URL, GWSW_API_URL

import requests
import zipfile
import json
import time
import arcpy
from osgeo import ogr, osr
import os


def get_bgt_features(extent_wkt, output_zip):
    """
    Download the bgt surfaces for a given extent from the PDOK API
    """
    try:
        data = {
            "featuretypes": list(ALL_USED_SURFACE_TYPES),
            "format": "gmllight",
            "geofilter": extent_wkt,
        }
        headers = {"Content-Type": "application/json"}

        r = requests.post(BGT_API_URL, data=json.dumps(data), headers=headers)
        download_id = r.json()["downloadRequestId"]
        status_link = BGT_API_URL + "/" + download_id + "/status"

        status = "PENDING"
        while status != "COMPLETED":
            request = requests.get(status_link)
            status = request.json()["status"]
            # if request.status_code >= 500:
            # 	# TODO of restricties vanuit Wifi! netwerk!
            # 	message = f"BGT API Server werkt niet zoals verwacht probeer het later nog eens status_code is {request.status_code}"
            # 	arcpy.AddError(message)
            # 	raise ValueError(message)
            # elif request.status_code >= 400:
            # 	message = f"Er is iets anders fout gegaan, status_code is {request.status_code}"
            # 	arcpy.AddError(message)
            # 	raise ValueError(message)
            time.sleep(5)

        download_url_extract = request.json()["_links"]["download"]["href"]
        download_url = "https://api.pdok.nl" + download_url_extract
        download_request = requests.get(download_url)

        with open(output_zip, "wb") as f:
            f.write(download_request.content)

    except Exception:
        import sys
        import traceback

        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        print("PYTHON ERRORS:\nTraceback info:\n" + tbinfo)
        print("############################")
        print("Error Info:\n" + str(sys.exc_info()[1]))
        print("einde!")

def get_gwsw_features(extent_wkt, output_gpkg):
    try:
        nwt = NetworkTask(CBS_GEMEENTES_API_URL, output_gpkg, extent_wkt, "default_lijn")
        nwt.run()
    except Exception:
        import sys
        import traceback

        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        print("PYTHON ERRORS:\nTraceback info:\n" + tbinfo)
        print("############################")
        print("Error Info:\n" + str(sys.exc_info()[1]))
        print("einde!")

def get_bag_features(extent_wkt, output_gpkg):
    try:
        nwt = NetworkTask(BAG_API_URL, output_gpkg, extent_wkt, "bag_panden")
        nwt.run()
    except Exception:
        import sys
        import traceback

        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        print("PYTHON ERRORS:\nTraceback info:\n" + tbinfo)
        print("############################")
        print("Error Info:\n" + str(sys.exc_info()[1]))
        print("einde!")

class NetworkTask():
    def __init__(self, url, output_gpkg, extent_geometry_wkt, layer_name):
        self.url = url
        self.output_gpkg = output_gpkg
        self.extent_geometry_wkt = extent_geometry_wkt
        self.extent_bbox = self.wkt_to_bbox()
        self.layer_name = layer_name
        
    def run(self):
        extent_geometry = ogr.CreateGeometryFromWkt(self.extent_geometry_wkt)
        bbox = self.wkt_to_bbox()
        all_features = self.fetch_all_features(bbox)
        self.save_features_to_gpkg(all_features, extent_geometry)
        return True
    
    def fetch_all_features(self, bbox):
        not_all_features_found = True
        index = 0
        all_features = []
    
        print("Fetching features within BBox")
        while not_all_features_found:
            request_url = self.url + f"&startIndex={index}" + f"&BBOX={bbox}"
            data = self.load_api_data(request_url, "")

            
            all_features.extend(data['features'])
            
            if len(data['features']) < 1000:
                not_all_features_found = False
            else:
                index += 1000
        
        return all_features
    
    def load_api_data(self, url,gemeente):
        response = requests.get(url)
        
        if response.status_code == 404:
            print(f"Error 404: {gemeente} not found.")
            return None
        
        return response.json()
    
    def save_features_to_gpkg(self, all_features, extent_geometry):
        print("Saving features to GeoPackage")
        
        driver = ogr.GetDriverByName("GPKG")
        if os.path.exists(self.output_gpkg):
            driver.DeleteDataSource(self.output_gpkg)
        datasource = driver.CreateDataSource(self.output_gpkg)
        
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(28992)
        
        if self.layer_name != "bag_panden":
            all_features = self.filter_features_by_extent(all_features, extent_geometry)
            all_features = self.fetch_gwsw_data(all_features)
    
        layer_out = self.create_layer(datasource, srs)
        self.add_features_to_layer(layer_out, all_features, extent_geometry)
        
        datasource = None
    
    def filter_features_by_extent(self, all_features, extent_geometry):
        selection_gemeentes = []
        
        for feature in all_features:
            geometry_wkt = self.geojson_to_wkt(feature['geometry'])
            geojson_geom = ogr.CreateGeometryFromWkt(geometry_wkt)
            if extent_geometry.Intersects(geojson_geom):
                selection_gemeentes.append(feature['properties']['naam'])
        
        return selection_gemeentes
    
    def fetch_gwsw_data(self, selection_gemeentes):
        all_features = []
        
        for gemeente_name in selection_gemeentes:
            gemeente_name = gemeente_name.title().replace(" ", "").replace("-", "")
            not_all_features_found = True
            index = 0
            print(f"Extracting data for gemeente {gemeente_name}")
            
            while not_all_features_found:
                request_url = f"https://geodata.gwsw.nl/geoserver/{gemeente_name}-default/wfs/?&request=GetFeature&typeName={gemeente_name}-default:default_lijn&srsName=epsg:28992&OutputFormat=application/json" + (f"&startIndex={index}" if index > 0 else "")
                data = self.load_api_data(request_url,gemeente_name)
                
                if data is None:
                    NOT_FOUND_GEMEENTES.append(gemeente_name)
                    break
                
                all_features.extend(data['features'])
                
                if len(data['features']) < 1000:
                    not_all_features_found = False
                else:
                    index += 1000
        
        return all_features
    
    def create_layer(self, datasource, srs):
        if self.layer_name == "bag_panden":
            return datasource.CreateLayer(self.layer_name, geom_type=ogr.wkbPolygon, srs=srs)
        else:
            return datasource.CreateLayer(self.layer_name, geom_type=ogr.wkbMultiLineString, srs=srs)
    
    def add_features_to_layer(self, layer_out, all_features, extent_geometry):
        if not all_features:
            return
        
        feature_example = all_features[0]
        feature_fields = list(feature_example['properties'].keys())
        
        for field_name in feature_fields:
            field_defn = ogr.FieldDefn(field_name, ogr.OFTString)  # Adjust field type as needed
            layer_out.CreateField(field_defn)
        
        layer_defn = layer_out.GetLayerDefn()
        
        print("Writing features to GeoPackage")
        for feature_data in all_features:
            geometry_wkt = self.geojson_to_wkt(feature_data['geometry'])
            geojson_geom = ogr.CreateGeometryFromWkt(geometry_wkt)
            if extent_geometry.Intersects(geojson_geom):
                out_feature = ogr.Feature(layer_defn)
                geometry = ogr.CreateGeometryFromJson(json.dumps(feature_data['geometry']))
                out_feature.SetGeometry(geometry)
                
                for field_name, field_value in feature_data['properties'].items():
                    field_index = layer_defn.GetFieldIndex(field_name)
                    if field_index != -1:
                        out_feature.SetField(field_name, field_value)
                layer_out.CreateFeature(out_feature)
                out_feature = None
    
    def wkt_to_bbox(self):
        
        geom = ogr.CreateGeometryFromWkt(self.extent_geometry_wkt)
        env = geom.GetEnvelope()
        return "%d,%d,%d,%d" %(env[0],env[2],env[1],env[3])
    
    def geojson_to_wkt(self,geojson):
        geom = ogr.CreateGeometryFromJson(str(geojson))
        return geom.ExportToWkt()


if __name__ == "__main__":

    extent_wkt =  "Polygon ((110870.34528933660476469 455397.70264967781258747, 110927.88217626001278404 454151.07009967073099688, 112143.82838657461979892 454139.56272228603484109, 112093.96308457433769945 455535.79117829399183393, 110870.34528933660476469 455397.70264967781258747))"
    output_zip = r"C:\GIS\test_data_inlooptool\test_bgt_download1.zip"
    output_bag = r"C:\Users\vdi\Downloads\inlooptool_test\bag.gpkg"
    output_gwsw = r"C:\Users\vdi\Downloads\inlooptool_test\gwsw.gpkg"
    # get_bgt_features(extent_wkt, output_zip)

    # get_bag_features(extent_wkt, output_bag)

    get_gwsw_features(extent_wkt, output_gwsw)

    print("Klaar!")