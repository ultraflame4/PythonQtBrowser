import os
from urllib import request
import urllib
from PyQt5 import QtWebEngineCore
from adblockparser import AdblockRules

from PyQtBrowser.logger import logger

url_blacklists = []

blacklist_source = 'https://easylist.to/easylist/easylist.txt'
p="./resources/blacklists/"

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

if not os.path.exists(p+"easylist.txt"):
    request.urlretrieve(blacklist_source,p+'easylist.txt')



with open(p+"easylist.txt",'r',encoding='utf-8') as f:
    raw_rules = f.readlines()
    rules = AdblockRules(raw_rules)

class WebEngineUrlRequestInterceptor(QtWebEngineCore.QWebEngineUrlRequestInterceptor):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.log = logger("UrlRequestInterceptor")

    def interceptRequest(self, info:QtWebEngineCore.QWebEngineUrlRequestInfo):
        # print("Intercepted: ",info.requestUrl())
        url = info.requestUrl().toString()
        if rules.should_block(url):
            self.log.info("Blocking url: "+url)
            info.block(True)
        pass


