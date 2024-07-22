import os

MESSAGE_CATEGORY = "BGT Inlooptool"
BGT_API_URL = "https://api.pdok.nl/lv/bgt/download/v1_0/full/custom"

INLOOPTABEL_STYLE = os.path.join(
    os.path.dirname(__file__), "style", "bgt_inlooptabel.qml"
)
PIPES_STYLE = os.path.join(os.path.dirname(__file__), "style", "gwsw_lijn.qml")
BGT_STYLE = os.path.join(os.path.dirname(__file__), "style", "bgt_oppervlakken.qml")