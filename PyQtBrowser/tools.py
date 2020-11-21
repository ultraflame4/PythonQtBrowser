import mimetypes
import re
import threading
import typing
from urllib import request, parse

from PyQt5 import QtCore, QtWidgets

from PyQt5.QtWebEngineWidgets import *

from .logger import logger


class DownloadHandler:
    downloadpath = "./downloads"
    log = logger("DownloadHandler")

    class downloadworker:
        def __init__(self, url: QtCore.QUrl, file_type):
            self.origin = url.url()
            self.mimetype = file_type
            self.file_ext = (lambda: x if (x := mimetypes.guess_extension(self.mimetype)) is not None else '')()
            self.filename = self.origin.split('/')[-1] + self.file_ext
            self.log = DownloadHandler.log.getChild("downloadWorker")

        def _download_progress(self, blocknum, block_size, size):
            readed_data = blocknum * block_size
            percentage = int(readed_data * 100 / size)

            t= f"from {self.origin} [{readed_data}/{size} ({percentage}%)]"
            self.log.done(f"Downloading... file '{self.filename}' {t}")

        def start(self):
            self.log.info(f"Beginning Download of File: '{self.filename}' [Type: {self.mimetype}] from Url: '{self.origin}'")
            self.log.info(f"Into directory {DownloadHandler.downloadpath} []")

            request.urlretrieve(url=self.origin,
                                filename=DownloadHandler.downloadpath + '/' + self.filename,
                                reporthook=self._download_progress
                                )

    @staticmethod
    def _worker(download):
        w = DownloadHandler.downloadworker(download.url(), download.mimeType())
        w.start()

    @staticmethod
    def request_download(download: QWebEngineDownloadItem):
        c_process = threading.Thread(target=DownloadHandler._worker, args=(download,))
        c_process.start()


# TODO: A Html Caching System
class HtmlRequestsManager:
    pass



class WebpageHandler:
    """
    Handles opening of tabs and sites
    """

    def __init__(self):
        self.load_site: typing.Callable = None
        self.search_barWidget: QtWidgets.QLineEdit = None
        self._page_history = []
        self._page_future = []
        self._current_url = None
        self.utils=None
        self.log: logger = None
        # URL to search when text is not url
        self.default_searchaddr = "https://www.google.com/search?q="

    @staticmethod
    def validate_url(str):
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

    def formaturl(self, url):
        if WebpageHandler.validate_url(url):
            if not re.match('(?:http|ftp|https)://', url):
                return 'https://{}'.format(url)
            return url

        else:
            return self.default_searchaddr + parse.quote(url)

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
        self.log.done(f"Validating futurepages (Current: {self._page_future})..")
        if len(self._page_future) != 0:
            if url != self._page_future[-1]:
                self._page_future.clear()
                self.log.done("Invalidated future_pages")

        self.log.info(f"futurepages left: {self._page_future})")

    def load_webpage(self, url, _history=True, _supress_load=False):
        self.log.info(f"Loading Url: {url} (Suprressed: {_supress_load}, History: {_history})")
        url = self.formaturl(url)

        if url != self._current_url:
            if not _supress_load:
                self.load_site(self.formaturl(url))
                self.invalidate_futurepages(url)

            if self._current_url != None and _history:
                self.log.done(f"Appending {self._current_url} to history")
                self._page_history.append(self._current_url)

            self._current_url = url

            # self.info = htmlinfo_maker(url)

    def load_lastpage(self):
        self.log.info("Attempting to load previous page...")
        try:
            url = self.get_lastpage()
            curl = self._current_url




        except IndexError:
            self.log.error("There is no lastpage!")

        else:
            self.log.ok("Successfully got previous page.. proceeding...")

            self.search_barWidget.setText(url)

            self.load_webpage(url, _history=False)
            self.log.done(f"Appending current url {curl} to _page_future : {str(self._page_future)}")
            self._page_future.append(curl)
            self.log.debug(f"Future pages: {self._page_future}")

    def url_changed(self, qurl: QtCore.QUrl):
        self.log.info(f"url change detected : {qurl.url()}")

        if self._current_url != qurl.url():
            self.log.debug(f"Change not caused by self, registering change...")

            self.load_webpage(qurl.url(), _supress_load=True)
            self.search_barWidget.setText(qurl.url())
            self._current_url = qurl.url()
            self.search_barWidget.setCursorPosition(0)


    def newTab(self, *args):
        self.log.info("calling open new tab method..")

        self.utils.BrowserTabManager.new_tab()

    def finished_load(self):

        self.log.ok("Finished loading of url: " + str(self._current_url))
