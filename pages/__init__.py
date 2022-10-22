from PyQt5.QtWidgets import QLabel, QPushButton

from page import Page


class HomePage(Page):
    def initUI(self):
        super().initUI('pages/home.ui')
        self.pushButton.clicked.connect(self.btnClicked)

    def btnClicked(self):
        self._parent.setPage(SecondPage(self._parent))


class SecondPage(Page):
    def initUI(self):
        super().initUI()
        QLabel('Second Page', self).move(50, 50)
        self.btn = QPushButton("go back 😹", self)
        self.btn.clicked.connect(self.btnClicked)
        self.btn.move(50, 100)

    def btnClicked(self):
        self._parent.setPage(HomePage(self._parent))
