from dataclasses import dataclass

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWebEngineWidgets import *

from . import tools, utils


@dataclass()
class widgets_container:
    tab_widget:utils.dumb_Tab=None






class utils_container:
    def __init__(self, tab_container, logger):
        self.log = logger
        self.WebpageHandler = tools.WebpageHandler()
        self.WebpageHandler.utils=self
        self.WebpageHandler.log = self.log.getChild("WebpageHandler")
        self.BrowserTabManager = tab_container
        self.widgets=widgets_container()
        self.home_website = None


class search_bar(QtWidgets.QWidget):
    def __init__(self, utils: utils_container):
        self.log = utils.log.getChild('search_bar')
        self.log.info("Initialising search_bar")
        super().__init__()

        self.utils = utils

        self.setContentsMargins(0, 0, 0, 0)
        self.log.debug("Setted config :margins")

        self.setFixedHeight(30)
        self.log.debug("Fixed height")

        self._layout = QtWidgets.QHBoxLayout()
        self.log.debug("Got new layout instance")

        self.log.debug("Grabbing new widget intances:")
        self.backbutton = QtWidgets.QPushButton("Back")
        self.log.debug("-backbutton")
        self.forwardbutton = QtWidgets.QPushButton("Front")
        self.log.debug("-forwardbutton")
        self.newTabButton = QtWidgets.QPushButton("+")
        self.log.debug("-newTabButton")
        self.newTabButton.setFixedSize(25, 20)
        self.log.debug("-newTabButton:fixed size")

        self.searchbutton = QtWidgets.QPushButton("Search")
        self.log.debug("-searchbutton")
        self.webaddressbar = QtWidgets.QLineEdit()
        self.log.debug("-webaddressbar")

        self.utils.WebpageHandler.search_barWidget = self.webaddressbar

        self.searchbutton.clicked.connect(self.search_button)
        self.backbutton.clicked.connect(self.utils.WebpageHandler.load_lastpage)
        self.forwardbutton.clicked.connect(self.utils.WebpageHandler.load_futurepage)
        self.newTabButton.clicked.connect(self.utils.WebpageHandler.newTab)

        self._layout.addWidget(self.backbutton, stretch=0, alignment=QtCore.Qt.AlignLeft)
        self._layout.addWidget(self.forwardbutton, stretch=0, alignment=QtCore.Qt.AlignLeft)
        self._layout.addWidget(self.newTabButton, alignment=QtCore.Qt.AlignLeft)
        self._layout.addWidget(self.webaddressbar, stretch=1)
        self._layout.addWidget(self.searchbutton, stretch=0, alignment=QtCore.Qt.AlignRight)

        self._layout.setSpacing(3)

        # pyside :self._layout.setMargin(0)
        # pyqt5
        self._layout.setContentsMargins(2, 3, 2, 3)

        self.setLayout(self._layout)

        self.log.ok()

    def search_button(self):
        url = self.webaddressbar.text()
        self.utils.WebpageHandler.load_webpage(url)


class webpage_display(QWebEngineView):
    def __init__(self, utils: utils_container, bar: QtWidgets.QProgressBar):
        super().__init__()
        self.log = utils.log.getChild("webpageDisplay")
        self.utils = utils
        self.utils.WebpageHandler.load_site = self.load_site
        self.resize(1280, 780)
        self.webpage = self.page()

        self.urlChanged.connect(self.utils.WebpageHandler.url_changed)
        self.webpage.profile().downloadRequested.connect(self.on_downloadReqeusted)
        self.webpage.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self.webpage.fullScreenRequested.connect(self.on_fullscreenreq)
        self.bar = bar
        self.loadProgress.connect(self.load_progress)
        self.loadFinished.connect(self.on_loadFinish)
        self.iconChanged.connect(self.onIconChange)

    def on_fullscreenreq(self, req: QWebEngineFullScreenRequest):
        req.accept()

    def on_downloadReqeusted(self, download):
        tools.DownloadHandler.request_download(download)

    def load_progress(self, Progress):
        self.log.debug(f"Loading - {Progress}%")
        self.bar.setValue(Progress)

    def load_site(self, url):
        self.load(QtCore.QUrl(url))

    def on_loadFinish(self):
        self.utils.widgets.tab_widget.setTabText(self.title())
        self.utils.widgets.tab_widget.setTabIcon(self.webpage.icon())
        self.utils.WebpageHandler.finished_load()
        self.bar.setValue(0)

    def onIconChange(self,QIcon_):
        self.log.info("Icon changed, setting new icon..")
        self.utils.widgets.tab_widget.setTabIcon(QIcon_)
        self.log.ok("New Icon set")
        pass

class BrowserTab(QtWidgets.QWidget):
    def __init__(self, utils: utils_container):
        self.log = utils.log
        self.log.info("Initialising..")
        super().__init__()

        self.utils = utils

        self._layout = QtWidgets.QVBoxLayout()

        self.log.debug("Created a new layout instance")
        self._layout.setAlignment(QtCore.Qt.AlignTop)
        self.log.debug("Configured layout alignment")

        self.search_bar_widget = search_bar(self.utils)
        self.log.debug("Created a searchbar instance")

        self.loading_bar = QtWidgets.QProgressBar()
        self.log.debug("Created progress bar instance")
        self.loading_bar.setContentsMargins(2, 3, 2, 2)
        self.loading_bar.setTextVisible(False)
        self.loading_bar.setFixedHeight(2)

        self.webpage_display = webpage_display(self.utils, self.loading_bar)
        self.log.debug("Created a webpage_display instance")

        self.log.debug("Configuring..:")
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.log.done("setContentMargins")

        self._layout.setSpacing(0)
        self.log.done("set spacing")

        self._layout.addWidget(self.search_bar_widget)
        self.log.done("Add search_bar instance")

        self._layout.addWidget(self.loading_bar, stretch=1)
        self.log.done("Add progress bar instance")

        self._layout.addWidget(self.webpage_display, stretch=1)
        self.log.done("Add webpage_display instance")

        self.setLayout(self._layout)
        self.log.done("setLayout")

        self.utils.WebpageHandler.load_webpage(self.utils.home_website)
        self.log.info("Opened default home_website")

        self.log.success()
        self.log.info("Successfuly initiated BrowserTab()")
