from PyQt5.QtWidgets import QWidget
from PyQt5 import uic


class PageContainer(QWidget):
    """Container for pages, which are widgets that can be switched between."""
    _page = None
    _previousPage = None

    def setPage(self, page):
        """Switches the current page to the given page.
        The previous page is stored to be able to go back."""
        if self._page:
            self._page.setParent(None)
        self._previousPage = self._page
        self._page = page
        self._page.setParent(self)
        self._page.setGeometry(0, 0, self.width(), self.height())
        self._page.show()
        self.setWindowTitle(
            self._page.windowTitle() + ' - quizzycat Desktop'
            if self._page.windowTitle()
            else 'quizzycat Desktop'
        )

    def previousPage(self):
        """Switches to the previous page if there is one."""
        if self._previousPage:
            self.setPage(self._previousPage)
            self._previousPage = None

    def resizeEvent(self, event):
        """Resizes the current page when the window is resized."""
        if self._page:
            self._page.setGeometry(0, 0, self.width(), self.height())

        super().resizeEvent(event)


class Page(QWidget):
    """Page is a widget that can be child of a PageContainer."""

    def __init__(self, parent: PageContainer):
        super().__init__(parent)
        self._parent = parent
        self.initUI()

    def initUI(self, ui: str = None):
        """Initialize UI from a .ui file."""
        if ui:
            uic.loadUi(ui, self)
