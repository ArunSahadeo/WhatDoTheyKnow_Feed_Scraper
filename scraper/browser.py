import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView

app = QApplication.instance() or QApplication(sys.argv)

class Browser(QWebEngineView):
    def __init__(self, url):
        #self.app = QApplication(sys.argv)
        QWebEngineView.__init__(self)
        self.html = None
        self.final_url = None
        self.loadFinished.connect(self._loadFinished)
        self.load(QUrl(url))
        #self.app.exec()
        app.exec()

    def _loadFinished(self, result):
        self.page().toHtml(self._storeHtml)

    def _storeHtml(self, html):
        self.html = html
        self.final_url = self.page().url().toString()
        #self.app.quit()
        app.quit()
