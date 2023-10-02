from peewee import *
import sys, os
dbPath = os.path.join(os.getcwd(), 'pattern.db')
db = SqliteDatabase(dbPath, field_types={'points': 'text'})