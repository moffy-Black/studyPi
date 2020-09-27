from datetime import datetime
import serial
import time
import RPi.GPIO as GPIO
import pyrebase
import json
import sqlite3

with open(('studyPi/firebaseConfig.json')) as f:
  firebaseConfig = json.loads(f.read())
firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

# GPIO_sensor
GPIO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN,GPIO.IN)

# connect flask_db
conn = sqlite3.connect('studyPi/studyPi.db')
c = conn.cursor()
c.execute("select * from users")
db_list = c.fetchone()

# ardino settings
ser = serial.Serial('/dev/ttyACM0', 9600)

# for time_measure value
start_time = None
array = [0]*5

if __name__ == '__main__':
  while True:
    if db_list is None:
      break
    for i in range(5):
      array[i] = GPIO.input(GPIO_PIN)
      time.sleep(1)
    if array[0] == GPIO.HIGH or array[1] == GPIO.HIGH or array[2] == GPIO.HIGH or  array[3] == GPIO.HIGH or  array[4] == GPIO.HIGH:
      if start_time is None:
        start_time = datetime.now()
      UNO_time = datetime.now()
      medium_time = UNO_time - start_time
      medium_second = medium_time.total_seconds()
      if medium_second <= 900:
        ser.write("a")
      elif medium_second >900 and medium_second <= 1800:
        ser.write("B")
      elif medium_second >1800 and medium_second <= :
        ser.write("c")
      elif medium_second >2700 and medium_second <= 3600:
        ser.write("d")
      elif medium_second >3600 and medium_second <= 4500:
        ser.write("e")
      elif medium_second >4500 and medium_second <= 5400:
        ser.write("f")
      elif medium_second >5400:
        ser.write("g")
      time.sleep(55)
    else:
      if start_time is None:
        time.sleep(55)
      else:
        finish_time = datetime.now()
        delta_time = finish_time - start_time
        delta_second = delta_time.total_seconds()
        start_time = None
        user_id = db_list[1]
        user_name = db_list[2]
        date = finish_time.strftime('%Y-%m-%d')
        term = delta_second // 60
        Ntime = finish_time.strftime('%H:%M')
        push_date = {
          "date": date,
          "name": user_name,
          "term": term,
          "time": Ntime
        }
        records = db.child("records").child(user_id).push(push_date)
        time.sleep(55)