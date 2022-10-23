import sqlite3

from db.models import User, Quiz, Question, Answer, Result


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('db.sqlite')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                passwordHash TEXT NOT NULL,
                passwordSalt TEXT NOT NULL,
                isTeacher INT NOT NULL,
                UNIQUE(username)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS quizzes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                authorId INTEGER NOT NULL,
                FOREIGN KEY (authorId) REFERENCES users(id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quizId INTEGER NOT NULL,
                question TEXT NOT NULL,
                multiple INT NOT NULL,
                FOREIGN KEY (quizId) REFERENCES quizzes(id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                questionId INTEGER NOT NULL,
                answer TEXT NOT NULL,
                isCorrect INT NOT NULL,
                FOREIGN KEY (questionId) REFERENCES questions(id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quizId INTEGER NOT NULL,
                userId INTEGER NOT NULL,
                score INTEGER NOT NULL,
                FOREIGN KEY (quizId) REFERENCES quizzes(id),
                FOREIGN KEY (userId) REFERENCES users(id)
            )
        ''')

        self.conn.commit()

    def pushUser(self, user: User):
        if user.id is not None:
            self.cursor.execute(
                '''
                    UPDATE 
                        users 
                    SET 
                        username = ?, 
                        passwordHash = ?, 
                        passwordSalt = ?, 
                        name = ?, 
                        surname = ?, 
                        isTeacher = ? 
                    WHERE 
                        id = ?
                ''', (
                    user.username,
                    user.passwordHash,
                    user.passwordSalt,
                    user.name,
                    user.surname,
                    user.isTeacher,
                    user.id
                )
            )
        else:
            self.cursor.execute('''
                INSERT INTO users (username, passwordHash, passwordSalt, name, surname, isTeacher)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user.username, user.passwordHash, user.passwordSalt, user.name, user.surname, user.isTeacher))

        self.conn.commit()

    def getUser(self, username):
        self.cursor.execute('''
            SELECT * FROM users WHERE username = ?
        ''', (username,))

        row = self.cursor.fetchone()
        if row is None:
            return None

        return User(row[1], row[2], row[3], row[4], row[5], row[6], id=row[0])

    def getAllUsers(self):
        self.cursor.execute('''
            SELECT * FROM users
        ''')

        rows = self.cursor.fetchall()
        if rows is None:
            return None

        users = []
        for row in rows:
            users.append(User(row[1], row[2], row[3], row[4], row[5], row[6], id=row[0]))

        return users

    def deleteUser(self, username):
        self.cursor.execute('''
            DELETE FROM users WHERE username = ?
        ''', (username,))

        self.conn.commit()

    def pushQuiz(self, quiz: Quiz):
        if quiz.id is not None:
            self.cursor.execute(
                '''
                    UPDATE quizzes SET name = ?, description = ?, authorId = ? WHERE id = ?
                ''', (
                    quiz.name,
                    quiz.description,
                    quiz.authorId,
                    quiz.id
                )
            )
        else:
            self.cursor.execute('''
                INSERT INTO quizzes (name, description, authorId)
                VALUES (?, ?, ?)
            ''', (quiz.name, quiz.description, quiz.authorId))

        self.conn.commit()

    def getQuiz(self, quizId):
        self.cursor.execute('''
            SELECT * FROM quizzes WHERE id = ?
        ''', (quizId,))

        row = self.cursor.fetchone()
        if row is None:
            return None

        return Quiz(row[1], row[2], row[3], id=row[0])

    def getAllQuizzes(self):
        self.cursor.execute('''
            SELECT * FROM quizzes
        ''')

        rows = self.cursor.fetchall()
        if rows is None:
            return None

        quizzes = []
        for row in rows:
            quizzes.append(Quiz(row[1], row[2], row[3], id=row[0]))

        return quizzes

    def deleteQuiz(self, quizId):
        self.cursor.execute('''
            DELETE FROM quizzes WHERE id = ?
        ''', (quizId,))

        self.conn.commit()

    def pushQuestion(self, question: Question):
        if question.id is not None:
            self.cursor.execute(
                '''
                    UPDATE questions SET quizId = ?, question = ?, multiple = ? WHERE id = ?
                ''', (
                    question.quizId,
                    question.question,
                    question.multiple,
                    question.id
                )
            )
        else:
            self.cursor.execute('''
                INSERT INTO questions (quizId, question, multiple)
                VALUES (?, ?, ?)
            ''', (question.quizId, question.question, question.multiple))

        self.conn.commit()

    def getQuestion(self, questionId):
        self.cursor.execute('''
            SELECT * FROM questions WHERE id = ?
        ''', (questionId,))

        row = self.cursor.fetchone()
        if row is None:
            return None

        return Question(row[1], row[2], row[3], id=row[0])

    def getAllQuestions(self, quizId):
        self.cursor.execute('''
            SELECT * FROM questions WHERE quizId = ?
        ''', (quizId,))

        rows = self.cursor.fetchall()
        if rows is None:
            return None

        questions = []
        for row in rows:
            questions.append(Question(row[1], row[2], row[3], id=row[0]))

        return questions

    def deleteQuestion(self, questionId):
        self.cursor.execute('''
            DELETE FROM questions WHERE id = ?
        ''', (questionId,))

        self.conn.commit()

    def pushAnswer(self, answer: Answer):
        if answer.id is not None:
            self.cursor.execute(
                '''
                    UPDATE answers SET questionId = ?, answer = ?, isCorrect = ? WHERE id = ?
                ''', (
                    answer.questionId,
                    answer.answer,
                    answer.isCorrect,
                    answer.id
                )
            )
        else:
            self.cursor.execute('''
                INSERT INTO answers (questionId, answer, isCorrect)
                VALUES (?, ?, ?)
            ''', (answer.questionId, answer.answer, answer.isCorrect))

        self.conn.commit()

    def getAnswer(self, answerId):
        self.cursor.execute('''
            SELECT * FROM answers WHERE id = ?
        ''', (answerId,))

        row = self.cursor.fetchone()
        if row is None:
            return None

        return Answer(row[1], row[2], row[3], id=row[0])

    def getAllAnswers(self, questionId):
        self.cursor.execute('''
            SELECT * FROM answers WHERE questionId = ?
        ''', (questionId,))

        rows = self.cursor.fetchall()
        if rows is None:
            return None

        answers = []
        for row in rows:
            answers.append(Answer(row[1], row[2], row[3], id=row[0]))

        return answers

    def deleteAnswer(self, answerId):
        self.cursor.execute('''
            DELETE FROM answers WHERE id = ?
        ''', (answerId,))

        self.conn.commit()

    def pushResult(self, result: Result):
        if result.id is not None:
            self.cursor.execute(
                '''
                    UPDATE results SET quizId = ?, userId = ?, score = ? WHERE id = ?
                ''', (
                    result.quizId,
                    result.userId,
                    result.score,
                    result.id
                )
            )
        else:
            self.cursor.execute('''
                INSERT INTO results (quizId, userId, score)
                VALUES (?, ?, ?)
            ''', (result.quizId, result.userId, result.score))

        self.conn.commit()

    def getResult(self, resultId):
        self.cursor.execute('''
            SELECT * FROM results WHERE id = ?
        ''', (resultId,))

        row = self.cursor.fetchone()
        if row is None:
            return None

        return Result(row[1], row[2], row[3], id=row[0])

    def getAllResults(self, quizId, userId):
        self.cursor.execute('''
            SELECT * FROM results WHERE quizId = ? AND userId = ?
        ''', (quizId, userId))

        rows = self.cursor.fetchall()
        if rows is None:
            return None

        results = []
        for row in rows:
            results.append(Result(row[1], row[2], row[3], id=row[0]))

        return results

    def deleteResult(self, resultId):
        self.cursor.execute('''
            DELETE FROM results WHERE id = ?
        ''', (resultId,))

        self.conn.commit()

