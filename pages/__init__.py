from datetime import datetime
from typing import List, Union

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QPushButton, QRadioButton, QCheckBox

from db.models import User, Quiz, Result
from forms import ManageQuizForm
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
        self._parent.setPage(DashboardPage(self._parent, user))


class DashboardPage(Page):
    def __init__(self, parent: PageContainer, user: User):
        self.user = user
        self.card_index = 0
        self.teacher = user.isTeacher
        self.quizzes = user.quizzes if self.teacher else Quiz.select()

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

        self.quizActionButton.clicked.connect(self.quizAction)
        self.quizResultsButton.clicked.connect(self.quizResults)

    def updateCard(self):
        if len(self.quizzes) == 0 and not self.teacher:
            self.quizNameLabel.setText('No quizzes available')
            self.quizDescriptionLabel.setText('')
            self.quizActionButton.hide()
            self.nextButton.hide()
            self.previousButton.hide()
            return

        self.quizResultsButton.show()
        self.quizActionButton.setText('Manage quiz' if self.teacher else 'Take quiz')
        if self.card_index >= len(self.quizzes) + (1 if self.teacher else 0):
            self.card_index = 0
        elif self.card_index < 0:
            self.card_index = len(self.quizzes) - (0 if self.teacher else 1)

        if self.teacher and self.card_index == len(self.quizzes):
            self.quizNameLabel.setText('Create new quiz')
            self.quizDescriptionLabel.setText('')
            self.quizActionButton.setText('Create')
            self.quizResultsButton.hide()
            return

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

    def quizAction(self):
        if self.teacher:
            self.manageQuizForm = ManageQuizForm(
                self.user,
                self.quizzes[self.card_index] if self.card_index < len(self.quizzes) else None
            )
            self.manageQuizForm.show()

        else:
            quiz = self.quizzes[self.card_index]
            print('Starting quiz', quiz.name)
            self._parent.setPage(QuizPage(self._parent, self.user, quiz))

    def quizResults(self):
        quiz = self.quizzes[self.card_index]
        print('Showing results for', quiz.name)
        # TODO: Show results

    def logout(self):
        self._parent.setPage(AuthPage(self._parent))


class QuizPage(Page):
    def __init__(self, parent: PageContainer, user: User, quiz: Quiz):
        self.user = user
        self.quiz = quiz
        self.questionIndex = 0
        self.answers = [None] * quiz.questions.count()
        super().__init__(parent)

    def initUI(self):
        super().initUI('pages/quiz.ui')

        self.setWindowTitle(self.quiz.name + ' - Quiz')

        btn = self.questionButton('?')
        btn.clicked.connect(lambda: self.goToQuestion(-1))
        self.questionList.addWidget(btn)

        for i, question in enumerate(self.quiz.questions):
            btn = self.questionButton(str(i + 1))
            btn.clicked.connect(lambda _, n=i: self.goToQuestion(n))

            self.questionList.addWidget(btn)
        self.questionList.addStretch()

        btn = self.questionButton('')
        btn.clicked.connect(lambda: self.goToQuestion(self.quiz.questions.count()))
        btn.setIcon(QIcon('assets/images/submit.png'))
        self.questionList.addWidget(btn)

        self.goToQuestion(-1)

        self.nextButton.clicked.connect(lambda _: self.goToQuestion(self.questionIndex + 1))

    def goToQuestion(self, index):
        self.questionIndex = index

        n = -1
        for i in range(self.questionList.count()):
            btn = self.questionList.itemAt(i).widget()
            if btn is None:
                continue
            if n == index:
                btn.setProperty('selected', True)
            else:
                btn.setProperty('selected', False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

            n += 1

        for i in reversed(range(self.answerList.count())):
            self.answerList.itemAt(i).widget().deleteLater()
        self.nextButton.show()

        if index == -1:
            self.titleLabel.setText(self.quiz.name)
            self.subtitleLabel.setText(self.quiz.description)
            self.nextButton.setText('Start')
        elif index == self.quiz.questions.count():
            self.nextButton.hide()

            self.titleLabel.setText('Submit')
            self.subtitleLabel.setText('Are you sure you want to submit?')

            btn = QPushButton('yup ✅✅✅')
            btn.clicked.connect(self.submit)
            btn.setStyleSheet('''
                QPushButton {
                    border-radius: 5px;
                    background-color: #000;
                    color: #fff;
                    padding: 10px;
                    font-size: 14px;
                }
                
                QPushButton:hover {
                    background-color: #111;
                }
            ''')
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            self.answerList.addWidget(btn)

            btn = QPushButton('i want to double check 🤔')
            btn.clicked.connect(lambda: self.goToQuestion(0))
            btn.setStyleSheet('''
                QPushButton {
                    border-radius: 5px;
                    background-color: #000;
                    color: #fff;
                    padding: 10px;
                    font-size: 14px;
                }
                
                QPushButton:hover {
                    background-color: #111;
                }
            ''')
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            self.answerList.addWidget(btn)
        else:
            question = self.quiz.questions[index]
            self.titleLabel.setText(question.text)
            self.subtitleLabel.setText(
                question.isMultipleChoice and 'Multiple answer' or 'Single answer'
            )
            self.nextButton.setText('Next')

            for i, answer in enumerate(self.quiz.questions[index].answers):
                btn = self.answerCheckbox(answer.text) if question.isMultipleChoice \
                    else self.answerRadioButton(answer.text)

                btn.clicked.connect(lambda _, n=i: self.answerSelected(n))

                if self.answers[index] is not None and (
                        question.isMultipleChoice and i in self.answers[index] or
                        not question.isMultipleChoice and i == self.answers[index]
                ):
                    btn.setChecked(True)

                self.answerList.addWidget(btn)

    def questionButton(self, text):
        btn = QPushButton(text)
        btn.setProperty('selected', False)
        btn.setStyleSheet('''
                QPushButton {
                    background-color: #fff;
                    border: 1px solid #000;
                    border-radius: 4px;
                    font-size: 10px;
                    font-weight: bold;
                    padding: 1px;
                }
                
                QPushButton:hover {
                    background-color: #eee;
                }   
                
                QPushButton[selected=true] {
                    background-color: #000;
                    color: #fff;
                }
            ''')
        btn.setFixedSize(24, 24)
        btn.setCursor(QCursor(Qt.PointingHandCursor))

        return btn

    def answerRadioButton(self, text):
        btn = QRadioButton(text)
        btn.setStyleSheet('''
            QRadioButton {
                font-size: 14px;
            }
        ''')
        btn.setCursor(QCursor(Qt.PointingHandCursor))
        return btn

    def answerCheckbox(self, text):
        btn = QCheckBox(text)
        btn.setStyleSheet('''
            QCheckBox {
                font-size: 14px;
            }
        ''')
        btn.setCursor(QCursor(Qt.PointingHandCursor))
        return btn

    def answerSelected(self, index):
        if self.quiz.questions[self.questionIndex].isMultipleChoice:
            self.answers[self.questionIndex] = [
                i for i in range(len(self.quiz.questions[self.questionIndex].answers))
                if self.answerList.itemAt(i).widget().isChecked()
            ]
        else:
            self.answers[self.questionIndex] = index

    def submit(self):
        print('Submitting quiz', self.quiz.name)
        self._parent.setPage(QuickResultsPage(self._parent, self.user, self.quiz, self.answers))


class QuickResultsPage(Page):
    def __init__(self, parent: PageContainer, user: User, quiz: Quiz, answers: List[Union[int, List[int], None]]):
        self.user = user
        self.quiz = quiz
        self.answers = answers

        super().__init__(parent)

    def initUI(self):
        super().initUI('pages/qresults.ui')

        score = 0
        max_score = 0
        for i, question in enumerate(self.quiz.questions):
            max_score += 1
            if self.answers[i] is None:
                continue

            if question.isMultipleChoice:
                if self.answers[i] == [i for i, a in enumerate(question.answers) if a.isCorrect]:
                    score += 1
            else:
                if question.answers[self.answers[i]].isCorrect:
                    score += 1

        self.scoreLabel.setText(f'Score: {score}/{max_score}')

        self.homeButton.clicked.connect(lambda: self._parent.setPage(DashboardPage(self._parent, self.user)))

        Result.create(
            user=self.user,
            quiz=self.quiz,
            score=score,
            date=datetime.now()
        )
