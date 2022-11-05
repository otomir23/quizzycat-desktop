import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QApplication

import db
from page import PageContainer
from pages import AuthPage


class App(PageContainer):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('quizzycat Desktop')
        self.resize(640, 480)
        self.setMinimumSize(self.size())
        self.show()

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        self.setPage(AuthPage(self))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()

    font_bold = QFontDatabase.addApplicationFont('assets/fonts/Inter-Bold.ttf')
    font_regular = QFontDatabase.addApplicationFont('assets/fonts/Inter-Medium.ttf')

    app.setFont(QFont('Inter', 10, QFont.Normal))

    status = app.exec_()
    db.db.close()
    sys.exit(status)
