import typing

from PyQt5 import QtCore,QtWidgets
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *
from . import tools


class BrowserTabManager:
    new_tab:typing.Callable = None


class utils_container:
    def __init__(self,tab_container):
        self.WebpageHandler = tools.WebpageHandler()
        self.WebpageHandler.BrowserHandler=BrowserTabManager

        self.BrowserTabContainer = tab_container
        self.home_website=None

class search_bar(QtWidgets.QWidget):
    def __init__(self,utils:utils_container):
        print("Initiating search_bar")
        super().__init__()
        print("Initiated parent class")

        self.utils = utils



        self.setContentsMargins(0,0,0,0)
        print("Setted config :margins")

        self.setFixedHeight(23)
        print("Fixed height")


        self._layout = QtWidgets.QHBoxLayout()
        print("Got new layout instance")


        print("Grabbing new widget intances:")
        self.backbutton = QtWidgets.QPushButton("Back")
        print("-backbutton")
        self.forwardbutton = QtWidgets.QPushButton("Front")
        print("-forwardbutton")
        self.newTabButton = QtWidgets.QPushButton("+")
        print("-newTabButton")
        self.newTabButton.setFixedSize(25,20)
        print("-newTabButton:fixed size")

        self.searchbutton = QtWidgets.QPushButton("Search")
        print("-searchbutton")
        self.webaddressbar = QtWidgets.QLineEdit()
        print("-webaddressbar")



        self.utils.WebpageHandler.search_barWidget = self.webaddressbar

        self.searchbutton.clicked.connect(self.search_button)
        self.backbutton.clicked.connect(self.utils.WebpageHandler.load_lastpage)
        self.forwardbutton.clicked.connect(self.utils.WebpageHandler.load_futurepage)
        self.newTabButton.clicked.connect(self.utils.WebpageHandler.newTab)


        self._layout.addWidget(self.backbutton,stretch=0,alignment=QtCore.Qt.AlignLeft)
        self._layout.addWidget(self.forwardbutton,stretch=0,alignment=QtCore.Qt.AlignLeft)
        self._layout.addWidget(self.newTabButton,alignment=QtCore.Qt.AlignLeft)
        self._layout.addWidget(self.webaddressbar,stretch=1)
        self._layout.addWidget(self.searchbutton,stretch=0,alignment=QtCore.Qt.AlignRight)


        self._layout.setSpacing(3)

        # pyside :self._layout.setMargin(0)
        # pyqt5
        self._layout.setContentsMargins(2,3,2,0)


        self.setLayout(self._layout)

    def search_button(self):
        url = self.webaddressbar.text()
        self.utils.WebpageHandler.load_webpage(url)






class webpage_display(QWebEngineView):
    def __init__(self,utils:utils_container):
        super().__init__()
        self.utils=utils
        self.utils.WebpageHandler.load_site = self.load_site
        self.resize(1280,780)
        self.webpage = self.page()


        self.urlChanged.connect(self.utils.WebpageHandler.url_changed)
        self.webpage.profile().downloadRequested.connect(self.on_downloadReqeusted)
        self.webpage.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled,True)
        self.webpage.fullScreenRequested.connect(self.on_fullscreenreq)


    def on_fullscreenreq(self,req:QWebEngineFullScreenRequest):
        req.accept()



    def on_downloadReqeusted(self,download):
        tools.downloadHandler.request_download(download)


    def load_site(self,url):
        self.load(QtCore.QUrl(url))


    def loadFinished(self, *args, **kwargs):
        print("Finished loading...")



class BrowserTab(QtWidgets.QWidget):
    def __init__(self,utils:utils_container):
        print("Initiating new tab")
        super().__init__()

        print("Initiated root")

        self.utils = utils

        self._layout = QtWidgets.QVBoxLayout()

        print("Got new layout instance")
        self._layout.setAlignment(QtCore.Qt.AlignTop)
        print("Setted layout alignment")

        self.search_bar_widget = search_bar(self.utils)
        print("Got searchbar instance")


        self.webpage_display = webpage_display(self.utils)
        print("Got webpage_display instance")


        print("Setting Configs")
        self._layout.setContentsMargins(0,0,0,0)
        print("Margine: Done")

        self._layout.setSpacing(4)
        print("Spacing: Done")

        self._layout.addWidget(self.search_bar_widget)
        print("Added search_bar instance")

        self._layout.addWidget(self.webpage_display,stretch=1)
        print("Added webpage_display instance")

        self.setLayout(self._layout)
        print("Added Layout")

        self.utils.WebpageHandler.load_webpage(self.utils.home_website)
        print("Opened default home_website")



        print("[ SUCCESS ] Successfuly initiated BrowserTab()")
