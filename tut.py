import sys
import PySide2 as qt
import PySide2.QtWebEngineWidgets
import PySide2.QtWebEngineCore
import PySide2.QtWidgets

app = qt.QtWidgets.QApplication()
web = qt.QtWebEngineWidgets.QWebEngineView()
web.load("https://www.reddit.com")

web.show()
sys.exit(app.exec_())