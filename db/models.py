class User:
    def __init__(self, username, passwordHash, passwordSalt, name, surname, isTeacher, id=None):
        self.id = id
        self.username = username
        self.passwordHash = passwordHash
        self.passwordSalt = passwordSalt
        self.name = name
        self.surname = surname
        self.isTeacher = isTeacher


class Quiz:
    def __init__(self, name, description, authorId, id=None):
        self.id = id
        self.name = name
        self.description = description
        self.authorId = authorId


class Question:
    def __init__(self, quizId, question, multiple, id=None):
        self.id = id
        self.quizId = quizId
        self.question = question
        self.multiple = multiple


class Answer:
    def __init__(self, questionId, answer, isCorrect, id=None):
        self.id = id
        self.questionId = questionId
        self.answer = answer
        self.isCorrect = isCorrect


class Result:
    def __init__(self, quizId, userId, score, id=None):
        self.id = id
        self.quizId = quizId
        self.userId = userId
        self.score = score
