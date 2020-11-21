import dataclasses
import logging
import sys
import typing
import re
import urllib
import mimetypes

from urllib import request
import threading
from urllib.request import urlopen

import bs4
import favicon
import requests
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from PyQtBrowser import utils


class downloadHandler:
    downloadpath="./downloads"

    class downloadWorker:
        def __init__(self,url:QtCore.QUrl,file_type,r_name=None):
            self.origin = url.url()
            self.mimetype=file_type
            self.file_ext = (lambda: x if (x:=mimetypes.guess_extension(self.mimetype)) != None else '')()
            self.filename = self.origin.split('/')[-1]+self.file_ext

        def _download_progress(self, blocknum, block_size, size):
            readed_data = blocknum * block_size
            percentage = int(readed_data* 100/size)
            print(f"Download Progress: [ {readed_data}/{size} ({percentage}%) | File:{self.filename} | Src : {self.origin}]")
            pass


        def start(self):
            print(f"Beginning Download of File: '{self.filename}' [Type: {self.mimetype}] from Url: '{self.origin}'")
            print(f"Into directory {downloadHandler.downloadpath} []")

            request.urlretrieve(url=self.origin,
                                filename=downloadHandler.downloadpath+'/'+self.filename,
                                reporthook=self._download_progress
                                )


    @staticmethod
    def _worker(download):
        w = downloadHandler.downloadWorker(download.url(), download.mimeType())
        w.start()
        print("Download finished")



    @staticmethod
    def request_download(download:QWebEngineDownloadItem):
        c_process = threading.Thread(target=downloadHandler._worker,args=(download,))
        c_process.start()



# TODO: A Html Caching System
class HtmlRequestsManager:
    pass






# A object to hold info abt the page
# eg, icons ,title ,desc
@dataclasses.dataclass
class HtmlInfo:
    src_url: str
    favicon: QIcon
    title: str









def htmlinfo_maker(url):

    soup = bs4.BeautifulSoup(requests.get(url).text,"lxml")



    pixmal = QPixmap()
    pixmal.loadFromData(urlopen(favicon.get(url)[0].url).read())
    icon = QIcon(pixmal)

    page_title = soup.find("title").get_text()

    return HtmlInfo(
        favicon=icon,
        title=page_title,
        src_url=url
        )








class WebpageHandler:
    """
    Handles opening of tabs and sites
    """

    def __init__(self):
        self.load_site: typing.Callable = None
        self.search_barWidget: QtWidgets.QLineEdit = None
        self._page_history = []
        self._page_future = []
        self._current_url=None
        self.BrowserHandler=None
        self.tab = None

        self.info: HtmlInfo = None
        self.log: logging.Logger=None
        # URL to search when text is not url
        self.default_searchaddr="https://www.google.com/search?q="





    def validate_url(self,str):
        # Regex to check valid URL
        regex = ("(www.)?" +
                 "[a-zA-Z0-9@:%._\\+~#?&//=]" +
                 "{2,256}\\.[a-z]" +
                 "{2,6}\\b([-a-zA-Z0-9@:%" +
                 "._\\+~#?&//=]*)")

        # Compile the ReGex
        p = re.compile(regex)

        # If the string is empty
        # return false
        if (str == None):
            return False

        # Return if the string
        # matched the ReGex
        if (re.search(p, str)):
            return True
        else:
            return False


    def formaturl(self,url):
        if self.validate_url(url):
            if not re.match('(?:http|ftp|https)://', url):
                return 'https://{}'.format(url)
            return url

        else:
            return self.default_searchaddr+urllib.parse.quote(url)

    def get_history(self):
        return self._page_history

    def get_lastpage(self):
        f = self._page_history.pop(-1)

        return f

    def load_futurepage(self):
        try:
            f = self._page_future.pop(-1)
            self.load_webpage(f)
        except IndexError:
            self.log.error("No future pages!")

    def invalidate_futurepages(self, url):
        self.log.info(f"Checking if futurepages are invalid (Current: {self._page_future})")
        if len(self._page_future) != 0:
            if url != self._page_future[-1]:
                self.log.info("Invalidating futurepages ...")
                self._page_future.clear()

        self.log.info(f"futurepages left: {self._page_future})")

    def load_webpage(self,url,_history=True,_supress_load=False):
        self.log.info(f"Loading Url: {url} (Suprressed: {_supress_load}, History: {_history})")
        url=self.formaturl(url)

        if url != self._current_url:
            if not _supress_load:
                self.load_site(self.formaturl(url))
                self.invalidate_futurepages(url)

            if self._current_url != None and _history:
                self._page_history.append(self._current_url)


            self.info = htmlinfo_maker(url)

    def load_lastpage(self):
        self.log.info("Attempting to load last page...")
        try:
            url = self.get_lastpage()
            curl = self._current_url




        except IndexError:
            self.log.error("There is no lastpage!")

        else:
            self.log.ok("Successfully got previous page.. proceeding...")



            self.search_barWidget.setText(url)

            self.load_webpage(url, _history=False)
            self.log.info(f"Appending current url {curl} to _page_future : {str(self._page_future)}")
            self._page_future.append(curl)
            self.log.info(f"Future pages: {self._page_future}")

    def url_changed(self,qurl:QtCore.QUrl):
        self.load_webpage(qurl.url(),_supress_load=True)
        self.search_barWidget.setText(qurl.url())
        self._current_url=qurl.url()
        self.search_barWidget.setCursorPosition(0)

        self.tab.setTabIcon(self.info.favicon)
        self.tab.setTabText(self.info.title)

    def newTab(self,*args):
        self.log.info("opening new tab..")

        self.BrowserHandler.new_tab()


    def finished_load(self):

        self.log.ok("Finished loading of url: "+str(self._current_url))