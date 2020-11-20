from PyQt5 import QtWebEngineCore

class WebEngineUrlRequestInterceptor(QtWebEngineCore.QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info:QtWebEngineCore.QWebEngineUrlRequestInfo):
        # print("Intercepted: ",info.requestUrl())

        pass


