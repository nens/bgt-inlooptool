import os

MESSAGE_CATEGORY = "BGT Inlooptool"

INLOOPTABEL_STYLE = os.path.join(
    os.path.dirname(__file__), "style", "bgt_inlooptabel.qml"
)
PIPES_STYLE = os.path.join(os.path.dirname(__file__), "style", "gwsw_lijn.qml")
BGT_STYLE = os.path.join(os.path.dirname(__file__), "style", "bgt_oppervlakken.qml")
INLOOPTABEL_STYLE_HIDDEN = os.path.join(os.path.dirname(__file__), "style", "bgt_inlooptabel_hidden.qml")
STATS_STYLE = os.path.join(os.path.dirname(__file__), "style", "stats.qml")
CHECKS_STYLE = os.path.join(os.path.dirname(__file__), "style", "checks.qml")
GPKG_TEMPLATE = os.path.join(os.path.dirname(__file__), "style", "template_output.gpkg")
GPKG_TEMPLATE_HIDDEN = os.path.join(os.path.dirname(__file__), "style", "template_output_hidden_fields.gpkg")

BGT_API_URL = "https://api.pdok.nl/lv/bgt/download/v1_0/full/custom"
BAG_API_URL = "https://service.pdok.nl/lv/bag/wfs/v2_0?service=WFS&version=2.0.0&request=GetFeature&typeName=bag:pand&outputFormat=application/json"
CBS_GEMEENTES_API_URL = "https://service.pdok.nl/kadaster/bestuurlijkegebieden/wfs/v1_0?service=WFS&version=1.0.0&request=GetFeature&typeName=Gemeentegebied&outputFormat=application/json"

NOT_FOUND_GEMEENTES = []  # Initialize the list for not found gemeentes (GWSW server)

