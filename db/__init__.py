from peewee import SqliteDatabase

db = SqliteDatabase('db.sqlite')
db.connect()
