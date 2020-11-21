from PyQt5 import QtWidgets

from . import browser_tab, utils
from .logger import logger


class dumb_Tab:
    def __init__(self, i, o):
        self.index = i
        self.o = o

    def setTabIcon(self, icon):
        self.o.setTabIcon(self.index, icon)

    def setTabText(self, text):
        self.o.setTabText(self.index, text)


class _BrowserTabs_container(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()
        self.log = logger("BrowserTabsContainer")

        self.log.info("Initialising BrowserTabsContainer")

        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.removeTab)
        browser_tab.BrowserTabManager.new_tab = self.OpenTab

    def getUtilsContainer(self, site):
        o = browser_tab.utils_container(self, self.log.getChild(f"BrowserTab({self.count()})"))
        o.home_website = site

        return o

    def setTabConfigs(self, index, info):
        pass

    def OpenTab(self, *args, site: str = 'www.google.com'):
        self.log.info(f"Opening new tab with website: {site}")

        utils.typecheck(str, site)

        self.log.info("Creating new 'BrowserTab' instance")
        o = browser_tab.BrowserTab(self.getUtilsContainer(site))
        self.log.info("Got new Instance successfully, adding tab..")
        i = self.addTab(o, o.webpage_display.utils.WebpageHandler.info.favicon,
                        o.webpage_display.utils.WebpageHandler.info.title)

        o.utils.WebpageHandler.tab = dumb_Tab(i, self)

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
