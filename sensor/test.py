from datetime import datetime
import time
import RPi.GPIO as GPIO
import pyrebase
import json
import sqlite3

with open(('studyPi/firebaseConfig.json')) as f:
  firebaseConfig = json.loads(f.read())
firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

def LED(n):
  for i in range(n):
    GPIO.output(li[i], True)
   
def RGB(x,y):
  GPIO.output(red_Pin, x)
  GPIO.output(green_Pin, y)
  GPIO.output(blue_Pin, False)

# GPIO_sensor
GPIO.setmode(GPIO.BCM)

GPIO_PIN = 18
Pin0 = 26
Pin1 = 19
Pin2 = 13
Pin3 = 10
Pin4 = 17
Pin5 = 12
red_Pin = 16
green_Pin = 20
blue_Pin = 21

GPIO.setup(GPIO_PIN,GPIO.IN)
GPIO.setup(Pin0,GPIO.OUT)
GPIO.setup(Pin1,GPIO.OUT)
GPIO.setup(Pin2,GPIO.OUT)
GPIO.setup(Pin3,GPIO.OUT)
GPIO.setup(Pin4,GPIO.OUT)
GPIO.setup(Pin5,GPIO.OUT)
GPIO.setup(red_Pin,GPIO.OUT)
GPIO.setup(green_Pin,GPIO.OUT)
GPIO.setup(blue_Pin,GPIO.OUT)

# connect flask_db
conn = sqlite3.connect('studyPi/studyPi.db')
c = conn.cursor()
c.execute("select * from users")
db_list = c.fetchone()

# for time_measure value
start_time = None
array = [0]*7
li = [Pin0,Pin1,Pin2,Pin3,Pin4,Pin5]
for i in range(6):
  GPIO.output(li[i], False)

if __name__ == '__main__':
  while True:
    if db_list is None:
      GPIO.cleanup()
      break
    for i in range(7):
      array[i] = GPIO.input(GPIO_PIN)
      time.sleep(1)
    if array[0] == GPIO.HIGH or array[1] == GPIO.HIGH or array[2] == GPIO.HIGH or  array[3] == GPIO.HIGH or  array[4] == GPIO.HIGH or array[5] == GPIO.HIGH or array[6] == GPIO.HIGH:
      if start_time is None:
        start_time = datetime.now()
      measure_time = datetime.now()
      medium_time = measure_time - start_time
      medium_second = medium_time.total_seconds()
      if medium_second <= 900:
        LED(6)
        RGB(False,True)
      elif medium_second >900 and medium_second <= 1800:
        LED(5)
        RGB(False,True)
      elif medium_second >1800 and medium_second <= 2700:
        LED(4)
        RGB(False,True)
      elif medium_second >2700 and medium_second <= 3600:
        LED(3)
        RGB(False,True)
      elif medium_second >3600 and medium_second <= 4500:
        LED(2)
        RGB(False,True)
      elif medium_second >4500 and medium_second <= 5400:
        LED(1)
        RGB(False,True)
      elif medium_second >5400:
        LED(0)
        RGB(False,True)
      time.sleep(53)
    else:
      if start_time is None:
        LED(0)
        RGB(True,False)
        time.sleep(53)
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
        conn = sqlite3.connect('studyPi/studyPi.db')
        c = conn.cursor()
        c.execute("select * from users")
        db_list = c.fetchone()
        LED(0)
        RGB(True,False)
        time.sleep(53)
