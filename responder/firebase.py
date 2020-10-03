import pyrebase
import json

with open(("firebaseConfig.json")) as f:
    firebaseConfig = json.loads(f.read())
firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()
db = firebase.database()