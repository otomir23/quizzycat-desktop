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
