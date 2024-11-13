import os

from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from bgtinlooptool.processing.bgt_surfaces_algorithm import BGTDownload2QgisAlgorithm


class BGTInloopToolProcessingProvider(QgsProcessingProvider):
    def id(self):
        return "bgt_inlooptool"

    def name(self):
        return "BGT Inlooptool"

    def icon(self):
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icon.png")
        return QIcon(icon_path)

    def load(self):
        self.refreshAlgorithms()
        return True

    def unload(self):
        QgsProcessingProvider.unload(self)
        self.algorithms_list = None

    def loadAlgorithms(self):
        self.addAlgorithm(BGTDownload2QgisAlgorithm())
