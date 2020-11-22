from PyQt5 import QtWidgets,QtGui,QtCore

from PyQtBrowser.logger import logger


class SettingsMenu(QtWidgets.QWidget):
    def __init__(self,log:logger):
        super().__init__()
        self.log = log.getChild("SettingsMenu")
        self.setMinimumSize(100,100)


    def show(self) -> None:

        QtWidgets.QWidget.show(self)