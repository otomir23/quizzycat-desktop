from peewee import Model, CharField, BooleanField, ForeignKeyField, IntegerField, DateTimeField

from db import db


class BaseModel(Model):
    """A base model that will use our SQLite database."""

    class Meta:
        database = db


class User(BaseModel):
    """A model that represents a user. A user can be a teacher or a student."""

    username = CharField()
    passwordHash = CharField()
    passwordSalt = CharField()
    name = CharField()
    surname = CharField()
    isTeacher = BooleanField()

    def checkPassword(self, password):
        from security import check_password
        return check_password(password, self.passwordHash, self.passwordSalt)


class Quiz(BaseModel):
    """A model that represents a quiz. A quiz can be created only by a teacher."""

    name = CharField()
    description = CharField()
    author = ForeignKeyField(User, backref='quizzes')


class Question(BaseModel):
    """A model that represents a question. A question can be linked with only one quiz."""

    quiz = ForeignKeyField(Quiz, backref='questions')
    text = CharField()
    isMultipleChoice = BooleanField()


class Answer(BaseModel):
    """A model that represents an answer. An answer can be linked with only one question."""

    question = ForeignKeyField(Question, backref='answers')
    text = CharField()
    isCorrect = BooleanField()


class Result(BaseModel):
    """A model that represents a result of a quiz completion by a student."""

    quiz = ForeignKeyField(Quiz, backref='results')
    user = ForeignKeyField(User, backref='results')
    score = IntegerField()
    date = DateTimeField()


# Create tables if they don't exist
db.create_tables([User, Quiz, Question, Answer, Result])

# Create teacher account if there are no teachers
if User.select().where(User.isTeacher == True).count() == 0:
    from security import generate_password_hash

    password_hash, password_salt = generate_password_hash('hackme')
    User.create(
        username='default',
        passwordHash=password_hash,
        passwordSalt=password_salt,
        name='Default',
        surname='Teacher',
        isTeacher=True
    )

# Create a student account if there are no students
# TODO this is temporary, until I implement user creation
if User.select().where(User.isTeacher == False).count() == 0:
    password_hash, password_salt = generate_password_hash('password')
    User.create(
        username='demo',
        passwordHash=password_hash,
        passwordSalt=password_salt,
        name='Demo',
        surname='Student',
        isTeacher=False
    )

