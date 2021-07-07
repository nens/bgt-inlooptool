"""
@author: Emile.deBadts
"""

SURFACE_TYPE_PAND = 'pand'
SURFACE_TYPE_WEGDEEL = 'wegdeel'
SURFACE_TYPE_ONDERSTEUNENDWEGDEEL = 'ondersteunendwegdeel'
SURFACE_TYPE_BEGROEIDTERREINDEEL = 'begroeidterreindeel'
SURFACE_TYPE_ONBEGROEIDTERREINDEEL = 'onbegroeidterreindeel'
SURFACE_TYPE_WATERDEEL = 'waterdeel'
SURFACE_TYPE_ONDERSTEUNENDWATERDEEL = 'ondersteunendwaterdeel'
SURFACE_TYPE_OVERIGBOUWWERK = 'overigbouwwerk'
SURFACE_TYPE_GEBOUWINSTALLATIE = 'gebouwinstallatie'
SURFACE_TYPE_OVERBRUGGINGSDEEL = 'overbruggingsdeel'

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
	SURFACE_TYPE_OVERBRUGGINGSDEEL
}

import requests
import zipfile
import json
import time
import arcpy


BGT_API_URL = 'https://api.pdok.nl/lv/bgt/download/v1_0/full/custom'


def get_bgt_api_surfaces(extent_wkt, output_zip):
	"""
	Download the bgt surfaces for a given extent from the PDOK API 
	"""
	try:
		data = {"featuretypes": list(ALL_USED_SURFACE_TYPES),
				"format": "gmllight",
				"geofilter": extent_wkt}
		headers = {'Content-Type': 'application/json'}

		r = requests.post(BGT_API_URL, data=json.dumps(data), headers=headers)
		download_id = r.json()['downloadRequestId']
		status_link = BGT_API_URL + '/' + download_id + '/status'

		status = 'PENDING'
		while status != 'COMPLETED':
			request = requests.get(status_link)
			status = request.json()['status']
			if request.status_code >= 500:
				message = f"BGT API Server werkt niet zoals verwacht probeer het later nog eens status_code is {request.status_code}"
				arcpy.AddError(message)
				raise ValueError(message)
			elif request.status_code >= 400:
				message = f"Er is iets anders fout gegaan, status_code is {request.status_code}"
				arcpy.AddError(message)
				raise ValueError(message)
			time.sleep(5)

		download_url_extract = request.json()['_links']['download']['href']
		download_url = 'https://api.pdok.nl' + download_url_extract
		download_request = requests.get(download_url)

		with open(output_zip, "wb") as f:
			f.write(download_request.content)

	except Exception:
		import sys
		import traceback

		tb = sys.exc_info()[2]
		tbinfo = traceback.format_tb(tb)[0]
		print("PYTHON ERRORS:\nTraceback info:\n" + tbinfo)
		print('############################')
		print("Error Info:\n" + str(sys.exc_info()[1]))
		print('einde!')


if __name__ == '__main__':

	extent_wkt = extent_polygon_wkt='Polygon ((110870.34528933660476469 455397.70264967781258747, 110927.88217626001278404 454151.07009967073099688, 112143.82838657461979892 454139.56272228603484109, 112093.96308457433769945 455535.79117829399183393, 110870.34528933660476469 455397.70264967781258747))'
	output_zip = r"C:\GIS\test_data_inlooptool\test_bgt_download1.zip"
	get_bgt_api_surfaces(extent_wkt, output_zip)

	print('Klaar!')





