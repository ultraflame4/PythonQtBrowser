from PyQt5 import QtWidgets,QtGui,QtCore

from PyQtBrowser.logger import logger


class ConfigMenuBase(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setAlignment(QtCore.Qt.AlignTop)


    def addWidget(self,w,font=None):
        (lambda : w if font is None else w.setFont(font))()
        self._layout.addWidget(w)
        return w




class generalConfigMenu(ConfigMenuBase):
    def __init__(self):
        super().__init__()

        self.toggle_adblock_checkbox = self.addWidget(QtWidgets.QCheckBox("Enable url blacklist"))




        self.setLayout(self._layout)

class ConfigMenu_container(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()
        self.general = generalConfigMenu()
        self.setTabBar(TabBar())
        self.setTabPosition(QtWidgets.QTabWidget.West)

        self.addTab(self.general,"General")




class SettingsMenu(QtWidgets.QWidget):
    def __init__(self,log:logger):
        super().__init__()
        self.log = log.getChild("SettingsMenu")
        self._layout = QtWidgets.QVBoxLayout()
        self.setStyle(ProxyStyle())
        self.container = ConfigMenu_container()
        self._layout.addWidget(self.container, stretch=1)
        self.setLayout(self._layout)
        self.setMinimumSize(100,100)

    def show(self) -> None:

        QtWidgets.QWidget.show(self)



















class TabBar(QtWidgets.QTabBar):
    def tabSizeHint(self, index):
        s = QtWidgets.QTabBar.tabSizeHint(self, index)
        s.transpose()
        return s

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        opt = QtWidgets.QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QtCore.QRect(QtCore.QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabLabel, opt);
            painter.restore()

class ProxyStyle(QtWidgets.QProxyStyle):
    def drawControl(self, element, opt, painter, widget):
        if element == QtWidgets.QStyle.CE_TabBarTabLabel:
            ic = self.pixelMetric(QtWidgets.QStyle.PM_TabBarIconSize)
            r = QtCore.QRect(opt.rect)
            w =  0 if opt.icon.isNull() else opt.rect.width() + self.pixelMetric(QtWidgets.QStyle.PM_TabBarIconSize)
            r.setHeight(opt.fontMetrics.width(opt.text) + w)
            r.moveBottom(opt.rect.bottom())
            opt.rect = r
        QtWidgets.QProxyStyle.drawControl(self, element, opt, painter, widget)