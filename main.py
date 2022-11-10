import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QFont, QIcon
from PyQt5.QtWidgets import QApplication

import db
from page import PageContainer
from pages import AuthPage


class App(PageContainer):
    """App is the main window of the application."""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Set up the main window. Set the window title, icon, size and the background color."""
        self.setWindowTitle('quizzycat Desktop')
        self.setWindowIcon(QIcon(
            'assets/images/icon.png'
        ))
        self.resize(640, 480)
        self.setMinimumSize(self.size())
        self.show()

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        self.setPage(AuthPage(self))


def except_hook(cls, exception, traceback):
    """Default exception hook."""
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()

    # Import font assets
    font_bold = QFontDatabase.addApplicationFont('assets/fonts/Inter-Bold.ttf')
    font_regular = QFontDatabase.addApplicationFont('assets/fonts/Inter-Medium.ttf')

    # Set default font
    app.setFont(QFont('Inter', 10, QFont.Normal))

    # Set default exception hook
    sys.excepthook = except_hook

    # Run the application
    status = app.exec_()

    # Close the database connection
    db.db.close()
    sys.exit(status)
