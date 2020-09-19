from datetime import datetime
import time
import RPi.GPIO as GPIO
import pyrebase
import json
import sqlite3

with open("./firebaseConfig.json") as f:
  firebaseConfig = json.loads(f.read())
firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

# for time_measure value

release = datetime.now()
T = 0
d = 0
flag = True
judge = True

# GPIO_sensor
GPIO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN,GPIO.IN)

# connect flask_db
conn = sqlite3.connect(r'/home/moffy/enviroment/flask/studyPi/studyPi.db')
c = conn.cursor()
c.execute("select * from users")
db_list = c.fetchone()
user_id = db_list[1]


if __name__ == '__main__':
  while flag:
    try:
      catch = datetime.now()
      while judge:
        if(GPIO.input(GPIO_PIN) == GPIO.HIGH):
          T += d
          d = 0
          time.sleep(1)
          print("Yes")
        else:
          release = datetime.now()
          DELTA = release - catch
          d = DELTA.total_seconds()
          if d >= 30.0:
            judge = False
          time.sleep(1)
          print("No")
    except KeyboardInterrupt:
      flag = False
      
    finally:
      s = T
      if s >= 10:
        date = release.strftime('%Y-%m-%d')
        term = s // 60
        Ntime = release.strftime('%H:%M')
        push_date = {
          "date": date,
          "term": term,
          "time": Ntime
        }
        # records = db.child("records").child(user_id).push(push_date)
      print(s)
      T = 0
      d = 0
      judge = True
  conn.close()
  GPIO.cleanup()

