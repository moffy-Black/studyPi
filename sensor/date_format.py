# import datetime
import pyrebase
import json
# s = 350
# m = s // 60
# h = m // 60
# value = m

# Now = datetime.datetime.now()
# year = Now.year
# month = Now.month
# day = Now.day
# date = str(year) + "-" + str(month) + "-" + str(day)
# print(value)
# print(Now.strftime('%Y-%m-%d'))
# print(Now.strftime('%H:%M'))

with open("./firebaseConfig.json") as f:
    firebaseConfig = json.loads(f.read())
firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
records = db.child("records").child("bz5pWlLkslU1TM7YReke8OSuxSM2").get()
print(records.val())