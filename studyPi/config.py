import os

SQLALCHEMY_DATABASE_URI = 'sqlite:///studyPi.db'
SECRET_KEY = os.urandom(24)