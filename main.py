import sys
import PyQtBrowser
from PyQtBrowser import request_intercepter
from PyQt5 import QtWebEngine,QtWebEngineWidgets,QtWebEngineCore


app = PyQtBrowser.QtWidgets.QApplication([])
urlintercept = request_intercepter.WebEngineUrlRequestInterceptor()
QtWebEngineWidgets.QWebEngineProfile.defaultProfile().setRequestInterceptor(urlintercept)
widget = PyQtBrowser.Browser()

widget.show()

sys.exit(app.exec_())