from PyQt5.QtWidgets import QWidget
from PyQt5 import uic


class PageContainer(QWidget):
    _page = None

    def setPage(self, page):
        if self._page:
            self._page.setParent(None)
        self._page = page
        self._page.setParent(self)
        self._page.setGeometry(0, 0, self.width(), self.height())
        self._page.show()

    def resizeEvent(self, event):
        if self._page:
            self._page.setGeometry(0, 0, self.width(), self.height())

        super().resizeEvent(event)


class Page(QWidget):
    def __init__(self, parent: PageContainer):
        super().__init__(parent)
        self._parent = parent
        self.initUI()

    def initUI(self, ui: str = None):
        if ui:
            uic.loadUi(ui, self)
