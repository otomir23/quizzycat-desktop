import sys
from PyQt5.QtWidgets import QApplication

from page import PageContainer

class App(PageContainer):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('quizzycat Desktop')
        self.resize(640, 480)
        self.setFixedSize(self.size())
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
