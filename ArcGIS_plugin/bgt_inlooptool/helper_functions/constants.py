from typing import NamedTuple, Union

import arcpy

BGT_API_URL = "https://api.pdok.nl/lv/bgt/download/v1_0/full/custom"
BAG_API_URL = "https://service.pdok.nl/lv/bag/wfs/v2_0?service=WFS&version=2.0.0&request=GetFeature&typeName=bag:pand&outputFormat=application/json"
GWSW_API_URL = "https://service.pdok.nl/rioned/beheerstedelijkwater/wfs/v1_0?service=WFS&version=2.0.0&request=GetFeature&typeName=beheerstedelijkwater:BeheerLeiding&outputFormat=application/json"
CBS_GEMEENTES_API_URL = "https://service.pdok.nl/kadaster/bestuurlijkegebieden/wfs/v1_0?service=WFS&version=1.0.0&request=GetFeature&typeName=Gemeentegebied&outputFormat=application/json"

NOT_FOUND_GEMEENTES = []  # Initialize the list for not found gemeentes (GWSW server)
WFS_FEATURE_LIMIT = 50000

class VisualizeLayer(NamedTuple):
    symbology_param: arcpy.Parameter
    visualize_field: Union[str, None]
    layer_name: str
    params_idx: int
    has_symbology: bool
