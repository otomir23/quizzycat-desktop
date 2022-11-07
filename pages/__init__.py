from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel

from db.models import User, Quiz
from page import Page, PageContainer


class AuthPage(Page):
    def initUI(self):
        super().initUI('pages/auth.ui')
        self.loginButton.clicked.connect(self.login)

    def login(self):
        self.errorLabel.setText('')

        username = self.usernameInput.text()
        password = self.passwordInput.text()

        if not username or not password:
            self.errorLabel.setText('Username and password are required')
            return

        user = User.select().where(User.username == username).first()

        if not user:
            self.errorLabel.setText('User not found')
            return

        if not user.checkPassword(password):
            self.errorLabel.setText('Incorrect password')
            return

        print('Logged in as', user.name, user.surname)
        if user.isTeacher:
            print('Teacher')
            # TODO: Go to teacher page
        else:
            self._parent.setPage(DashboardPage(self._parent, user))


class DashboardPage(Page):
    def __init__(self, parent: PageContainer, user: User):
        self.user = user
        self.card_index = 0
        self.quizzes = Quiz.select()
        super().__init__(parent)

    def initUI(self):
        super().initUI('pages/dashboard.ui')

        self.usernameLabel.setText(self.user.name + ' ' + self.user.surname)
        self.logoutButton.clicked.connect(self.logout)
        self.logoutButton.setIcon(QIcon('assets/images/logout.png'))

        self.updateCard()

        self.nextButton.clicked.connect(self.nextCard)
        self.nextButton.setIcon(QIcon('assets/images/next.png'))
        self.previousButton.clicked.connect(self.previousCard)
        self.previousButton.setIcon(QIcon('assets/images/previous.png'))

        self.quizStartButton.clicked.connect(self.startQuiz)


    def updateCard(self):
        if len(self.quizzes) == 0:
            self.quizNameLabel.setText('No quizzes available')
            self.quizDescriptionLabel.setText('')
            self.quizStartButton.hide()
            self.nextButton.hide()
            self.previousButton.hide()
            return

        if self.card_index >= len(self.quizzes):
            self.card_index = 0
        elif self.card_index < 0:
            self.card_index = len(self.quizzes) - 1

        quiz = self.quizzes[self.card_index]
        self.quizNameLabel.setText(quiz.name)
        description = quiz.description
        if len(description) > 100:
            description = description[:100] + '...'
        self.quizDescriptionLabel.setText(description)

    def nextCard(self):
        self.card_index += 1
        self.updateCard()

    def previousCard(self):
        self.card_index -= 1
        self.updateCard()

    def startQuiz(self):
        quiz = self.quizzes[self.card_index]
        print('Starting quiz', quiz.name)
        # TODO: Go to quiz page

    def logout(self):
        self._parent.setPage(AuthPage(self._parent))