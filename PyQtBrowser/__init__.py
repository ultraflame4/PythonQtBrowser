from PyQt5 import QtWidgets, QtGui

from . import browser_tab, utils, configuration
from .logger import logger


class _BrowserTabs_container(QtWidgets.QTabWidget):
    def __init__(self, browser, l:logger):
        super().__init__()
        self.Browser = browser
        self.log = l.getChild("BrowserTabsContainer")

        self.defaultFaviconQicon = browser.resources.favicon_qicon



        self.log.info("Initialising BrowserTabsContainer")

        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.removeTab)


    def getUtilsContainer(self, site):
        o = browser_tab.utils_container(self, self.log.getChild(f"BrowserTab({self.count()})"))
        o.home_website = site

        return o

    def OpenTab(self, *args, site: str = 'www.google.com'):
        self.log.info(f"Creating new tab with website: {site} opened")

        utils.typecheck(str, site)

        self.log.verbose("Creating new 'BrowserTab' instance")
        o = browser_tab.BrowserTab(self.getUtilsContainer(site))
        self.log.done("Got new Instance successfully, adding tab..")
        i = self.addTab(o, self.defaultFaviconQicon, 'untitled')
        self.log.done("Added tab")
        o.utils.widgets.tab_widget = utils.dumb_Tab(i, self)
        self.log.verbose("Created a dumb_tab instances and assigned to utils.widget.tab_widget instance attribute")


class Browser(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.log = logger("Browser")
        self.log.info("Initialising")

        self.resources : utils.resourceManager = utils.resourceManager()

        self._layout = QtWidgets.QVBoxLayout()


        self._layout.setSpacing(1)
        self._layout.setContentsMargins(3, 5, 3, 3)

        self.SettingsMenu = configuration.SettingsMenu(self.log)


        self.container = _BrowserTabs_container(self,self.log)


        self.container.OpenTab()

        self.container._layout = self._layout

        self._layout.addWidget(self.container)

        self.setLayout(self._layout)

        self.log.verbose("Setted layout")

        self.log.success("Successfully initiated instance")