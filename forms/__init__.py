import csv

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox

from db.models import Quiz, User, Question, Answer
from db import db
from util import resource_path


class ManageQuizForm(QWidget):
    """Form for creating and editing quizzes. If a quiz is given, the form will be filled with the quiz's data.
    If no quiz is given, the form will be empty and the user can create a new quiz."""

    def __init__(self, user: User, quiz: Quiz = None):
        self.user = user
        self.quiz = quiz
        self.questions = None

        super().__init__()
        self.initUI()

    def initUI(self):
        """Initialize UI from a .ui file."""

        self.setWindowTitle('Create quiz')
        self.setFixedSize(400, 300)
        self.setWindowIcon(QIcon(
            resource_path('assets/images/icon.png')
        ))

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        uic.loadUi(resource_path('forms/quiz_manage.ui'), self)

        self.loadButton.clicked.connect(self.loadQuestions)
        self.loadButton.setIcon(QIcon(resource_path('assets/images/import.png')))

        self.deleteButton.clicked.connect(self.delete)
        self.deleteButton.setIcon(QIcon(resource_path('assets/images/delete.png')))

        self.saveButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

        if self.quiz:
            self.nameEdit.setText(self.quiz.name)
            self.descriptionEdit.setText(self.quiz.description)

    def accept(self):
        """Save the quiz. If the quiz is new, it will be created."""

        if self.nameEdit.text().strip() == '':
            # Display an error dialog
            QMessageBox.critical(
                self,
                'Error',
                'The quiz must have a name.'
            )

            return

        if self.quiz is None:
            self.quiz = Quiz.create(
                name=self.nameEdit.text(),
                description=self.descriptionEdit.toPlainText(),
                author=self.user
            )
        else:
            self.quiz.name = self.nameEdit.text()
            self.quiz.description = self.descriptionEdit.toPlainText()
            self.quiz.save()

        db.commit()

        # Save the questions
        if self.questions:
            # Clear the existing questions and answers using a recursive delete
            Question.delete().where(Question.quiz == self.quiz).execute()
            Answer.delete().where(Answer.question << Question.select()).execute()

            for question in self.questions:
                q = Question.create(
                    quiz=self.quiz,
                    text=question['question'],
                    isMultipleChoice=question['is_multiple_choice']
                )

                for n, answer in enumerate(question['answers']):
                    Answer.create(
                        question=q,
                        text=answer,
                        isCorrect=(n in question['correct_answers'])
                    )

            db.commit()
        self.close()

    def reject(self):
        """Close the form without saving."""

        self.close()

    def loadQuestions(self):
        """Load questions from a file."""

        # Use built-in file dialog to select a file
        filename, _ = QFileDialog.getOpenFileName(
            self,
            'Select a file',
            '',
            'CSV files (*.csv)'
        )

        if filename:
            backup_questions = self.questions[:] if self.questions else None
            try:
                # Open the file using built-in CSV dict reader
                with open(filename, 'r', encoding='UTF-8') as f:
                    reader = csv.DictReader(f)

                    # Check if the file has the correct format
                    if set(reader.fieldnames) != {'question', 'answers', 'is_multiple_choice', 'correct_answers'}:
                        # Display an error dialog
                        QMessageBox.critical(
                            self,
                            'Error',
                            'The file is missing or has incorrect columns.'
                        )

                        return

                    # Read the questions
                    for row in reader:
                        # Convert the string values to the correct types
                        question = row['question']
                        answers = row['answers'].split(',')
                        is_multiple_choice = bool(int(row['is_multiple_choice']))
                        correct_answers = list(map(lambda r: int(r) - 1, row['correct_answers'].split(',')))

                        if self.questions is None:
                            self.questions = []

                        self.questions.append({
                            'question': question,
                            'answers': answers,
                            'is_multiple_choice': is_multiple_choice,
                            'correct_answers': correct_answers
                        })

                    # Display a message box
                    QMessageBox.information(
                        self,
                        'Success',
                        f'Loaded {len(self.questions)} questions.'
                    )

            except Exception as e:
                print(e)

                # Display an error dialog
                QMessageBox.critical(
                    self,
                    'Error',
                    'Unable to load or parse the file.'
                )

                self.questions = backup_questions

    def delete(self):
        """Delete the quiz."""

        # Display a confirmation dialog
        if QMessageBox.question(
            self,
            'Confirm',
            'Are you sure you want to delete this quiz? This action cannot be undone.',
            QMessageBox.Yes | QMessageBox.No
        ) == QMessageBox.Yes:
            # Delete the quiz
            if self.quiz is not None:
                self.quiz.delete_instance(recursive=True)
                db.commit()

            self.close()
