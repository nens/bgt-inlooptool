"""
Script Name: BGT Inloop Toolbox voor ArcGIS
Description: BGT Inloop Toolbox voor ArcGIS
Created By: Sjoerd Hoekstra
Date: 29/09/2020
"""
from bgt_inlooptool.bgt_inlooptool_ArcGIS import BGTInloopToolArcGIS
from bgt_inlooptool.bgt_vlakken_wfs import BgtVlakkenWFS


class Toolbox(object):

    def __init__(self):
        self.label = 'BGT Inloop Toolbox voor ArcGIS'
        self.alias = 'Toolbox'
        self.description = 'BGT Inloop Toolbox voor ArcGIS'

        # Explicitly define tools here.
        self.tools = [BGTInloopToolArcGIS]
