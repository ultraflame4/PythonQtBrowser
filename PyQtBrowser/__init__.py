from PyQt5 import QtWidgets, QtGui

from . import browser_tab, utils
from .logger import logger




class _BrowserTabs_container(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()
        self.log = logger("BrowserTabsContainer")

        pixMal = QtGui.QPixmap("./resources/favicon.png")
        self.tmpQicon = QtGui.QIcon(pixMal)



        self.log.info("Initialising BrowserTabsContainer")

        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.removeTab)


        browser_tab.BrowserTabManager.new_tab = self.OpenTab

    def getUtilsContainer(self, site):
        o = browser_tab.utils_container(self, self.log.getChild(f"BrowserTab({self.count()})"))
        o.home_website = site

        return o

    def OpenTab(self, *args, site: str = 'www.google.com'):
        self.log.info(f"Opening new tab with website: {site}")

        utils.typecheck(str, site)

        self.log.info("Creating new 'BrowserTab' instance")
        o = browser_tab.BrowserTab(self.getUtilsContainer(site))
        self.log.info("Got new Instance successfully, adding tab..")
        i = self.addTab(o,self.tmpQicon, 'untitled')

        o.utils.widgets.tab_widget = utils.dumb_Tab(i, self)

    def _getid(self):
        r = self._tabId_counter
        self._tabId_counter += 1
        return r


class Browser(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(1)
        self._layout.setContentsMargins(3, 5, 3, 3)

        self.container = _BrowserTabs_container()

        self.container.OpenTab()

        self.container._layout = self._layout

        self._layout.addWidget(self.container)
        self.setLayout(self._layout)
