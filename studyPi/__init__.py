from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pyrebase
import json

app = Flask(__name__)
app.config.from_object('studyPi.config')

db = SQLAlchemy(app)

import studyPi.views