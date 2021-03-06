from PyQt5 import QtGui


def typecheck(type_,val):
    if type(val) != type_:
        print(f"Value Error: Needed {type_} got {type(val)}!")
        raise ValueError(f"Needed {type_} got {type(val)}")



class dumb_Tab:
    def __init__(self, i, o):
        self.index = i
        self.o = o

    def setTabIcon(self, icon):
        self.o.setTabIcon(self.index, icon)

    def setTabText(self, text):
        self.o.setTabText(self.index, text)



class resourceManager:
    def __init__(self):
        self.path = './resources'

        self.favicon_pixmap = QtGui.QPixmap(f"{self.path}/favicon.png").scaledToHeight(10)
        self.favicon_qicon = QtGui.QIcon(self.favicon_pixmap)

        self.settings_pixmap = QtGui.QPixmap("./resources/settings.png").scaledToHeight(14)
        self.settings_qicon = QtGui.QIcon(self.settings_pixmap)

