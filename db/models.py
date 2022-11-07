from peewee import Model, CharField, BooleanField, ForeignKeyField, IntegerField, DateTimeField

from db import db


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
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
    name = CharField()
    description = CharField()
    author = ForeignKeyField(User, backref='quizzes')


class Question(BaseModel):
    quiz = ForeignKeyField(Quiz, backref='questions')
    text = CharField()
    isMultipleChoice = BooleanField()


class Answer(BaseModel):
    question = ForeignKeyField(Question, backref='answers')
    text = CharField()
    isCorrect = BooleanField()


class Result(BaseModel):
    quiz = ForeignKeyField(Quiz, backref='results')
    user = ForeignKeyField(User, backref='results')
    score = IntegerField()
    date = DateTimeField()


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
