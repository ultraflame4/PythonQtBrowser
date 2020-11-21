import typing

from PyQt5 import QtCore,QtWidgets
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *
import logging,colorama
from . import browser_tab, utils


reset = colorama.Fore.RESET + colorama.Fore.WHITE + colorama.Style.BRIGHT
clrs = colorama.Fore
style = colorama.Style

logging.addLevelName(25,"SUCCESS")
logging.addLevelName(23,"OK")

class logFilter(logging.Filter):
    def filter(self, record) -> int:
        record.levelnameCap = record.levelname.upper()
        return True




class formatter(logging.Formatter):
    levelColors = {
        "DEBUG":clrs.CYAN,
        "INFO": clrs.LIGHTGREEN_EX,
        "OK":clrs.GREEN,
        "SUCCESS":clrs.GREEN,
        "WARNING":clrs.YELLOW,
        "ERROR": clrs.RED,
        "CRITICAL":clrs.LIGHTRED_EX
        }
    def __init__(self,format):
        logging.Formatter.__init__(self,format)


    @staticmethod
    def formatString(string,color=clrs.WHITE,style_=style.NORMAL):
        return reset + style_ + color + string + reset


    def format(self, record: logging.LogRecord) -> str:
        lvl= record.levelname
        color = formatter.levelColors[lvl.upper()]


        record.levelnameCap = formatter.formatString(lvl.upper(), color, style.BRIGHT)
        record.levelname = formatter.formatString(
            (lambda :lvl.lower() if not lvl in ("OK","SUCCESS") else lvl.upper())()
            ,color)

        if record.funcName in ("__init__",):
            record.funcName=record.funcName.replace("_",'')





        record.name = "[" + record.name + "]"

        s = reset+logging.Formatter.format(self,record)
        return s


class logger(logging.Logger):
    FORMAT = "[%(levelnameCap)s] %(name)s %(funcName)s - %(levelname)s: %(message)s\n"

    def __init__(self,name,f=False,*args):
        logging.Logger.__init__(self,name,logging.INFO)
        console = logging.StreamHandler()
        fmt = formatter(logger.FORMAT)
        # console.addFilter(logFilter())
        console.setFormatter(fmt)

        self.addHandler(console)

    def ok(self,msg='',*args,**kwargs):
        self._log(23,msg,args,**kwargs)

    def success(self,msg='',*args,**kwargs):
        self._log(25,msg,args,**kwargs)


    def getChild(self, suffix: str):
        n = '] ['.join((self.name,suffix))
        return logger(n)


class dumb_Tab:
    def __init__(self,i,o):
        self.index=i
        self.o=o

    def setTabIcon(self, icon):
        self.o.setTabIcon(self.index,icon)

    def setTabText(self,text):
        self.o.setTabText(self.index,text)


class _BrowserTabs_container(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()
        self.log = logger("BrowserTabsContainer")

        self.log.info("Initialising BrowserTabsContainer")

        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.removeTab)
        browser_tab.BrowserTabManager.new_tab = self.OpenTab


    def getUtilsContainer(self,site):
        o = browser_tab.utils_container(self,self.log.getChild(f"BrowserTab({self.count()})"))
        o.home_website=site



        return o

    def setTabConfigs(self,index,info):
        pass


    def OpenTab(self,*args,site:str='www.google.com'):
        self.log.info(f"Opening new tab with website: {site}")

        utils.typecheck(str,site)


        self.log.info("Creating new 'BrowserTab' instance")
        o = browser_tab.BrowserTab(self.getUtilsContainer(site))
        self.log.info("Got new Instance successfully, adding tab..")
        i = self.addTab(o,o.webpage_display.utils.WebpageHandler.info.favicon,
                    o.webpage_display.utils.WebpageHandler.info.title)

        o.utils.WebpageHandler.tab=dumb_Tab(i,self)



    def _getid(self):
        r = self._tabId_counter
        self._tabId_counter += 1
        return r



class Browser(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(1)
        self._layout.setContentsMargins(3,5,3,3)


        self.container = _BrowserTabs_container()

        self.container.OpenTab()


        self.container._layout = self._layout

        self._layout.addWidget(self.container)
        self.setLayout(self._layout)