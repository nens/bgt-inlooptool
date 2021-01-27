"""
Script Name: BGT Inloop Toolbox voor ArcGIS
Description: BGT Inloop Toolbox voor ArcGIS
Created By: Sjoerd Hoekstra
Date: 29/09/2020
"""
from bgt_inlooptool.bgt_inlooptool_ArcGIS import BGTInloopToolArcGIS
from bgt_inlooptool.bgt_inlooptool_ArcGIS_test import BGTInloopToolArcGIS_test
# installs the gdal wheel for python 2 if not installed?
# TODO is python always installed for ArcGIS Pro?
from installs.install_packages import try_install_gdal
try_install_gdal()


class Toolbox(object):

    def __init__(self):
        self.label = 'BGT Inloop Toolbox voor ArcGIS'
        self.alias = 'Toolbox'
        self.description = 'BGT Inloop Toolbox voor ArcGIS'

        # Explicitly define tools here.
        self.tools = [BGTInloopToolArcGIS, BGTInloopToolArcGIS_test]
