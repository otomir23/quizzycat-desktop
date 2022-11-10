from peewee import SqliteDatabase

# Creating a database connection
db = SqliteDatabase('db.sqlite')
db.connect()
