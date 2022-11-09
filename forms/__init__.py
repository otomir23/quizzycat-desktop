from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget

from db.models import Quiz, User
from db import db


class ManageQuizForm(QWidget):
    def __init__(self, user: User, quiz: Quiz = None):
        self.user = user
        self.quiz = quiz

        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Create quiz')
        self.setFixedSize(400, 300)
        self.setWindowIcon(QIcon(
            'assets/images/icon.png'
        ))

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        # uic.loadUi('forms/quiz_manage.ui', self)
        # TODO: Create quiz_manage.ui

    def accept(self):
        if self.quiz is None:
            Quiz.create(
                name=self.nameEdit.text(),
                description=self.descriptionEdit.toPlainText(),
                author=self.user
            )
        else:
            self.quiz.name = self.nameEdit.text()
            self.quiz.description = self.descriptionEdit.toPlainText()
            self.quiz.save()

        db.commit()
        self.close()

    def reject(self):
        self.close()
