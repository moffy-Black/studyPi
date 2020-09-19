from datetime import datetime
import time
import RPi.GPIO as GPIO
import pyrebase
import json
import sqlite3

with open((r'/home/moffy/enviroment/flask/studyPi/firebaseConfig.json')) as f:
  firebaseConfig = json.loads(f.read())
firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

# GPIO_sensor
GPIO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN,GPIO.IN)

# connect flask_db
conn = sqlite3.connect(r'/home/moffy/enviroment/flask/studyPi/studyPi.db')
c = conn.cursor()
c.execute("select * from users")
db_list = c.fetchone()

starttime = datetime.now()
finishtime = datetime.now()
array = [0]*5

if __name__ == '__main__':
  while True:
    if db_list is None:
      break
    for i in range(5):
      array[i] = GPIO.input(GPIO_PIN)
      time.sleep(1)
    if array[0] == GPIO.HIGH or array[1] == GPIO.HIGH or array[2] == GPIO.HIGH or  array[3] == GPIO.HIGH or  array[4] == GPIO.HIGH:
      time.sleep(55)
    else:
      finishtime = datetime.now()
      deltatime = finishtime - starttime
      deltasecond = deltatime.total_seconds()
      if deltasecond >= 60:
        print(deltasecond)
        user_id = db_list[1]
        date = finishtime.strftime('%Y-%m-%d')
        term = deltasecond // 60
        Ntime = finishtime.strftime('%H:%M')
        push_date = {
          "date": date,
          "term": term,
          "time": Ntime
        }
        records = db.child("records").child(user_id).push(push_date)
        time.sleep(55)
      else:
        time.sleep(55)