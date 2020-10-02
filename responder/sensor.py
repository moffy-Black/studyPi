from datetime import datetime
import time
import RPi.GPIO as GPIO
import pyrebase
import json
import sqlite3

with open(('firebaseConfig.json')) as f:
  firebaseConfig = json.loads(f.read())
firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

def LED(n):
  li = [26,19,13,10,17,12]
  for i in range(6):
    GPIO.output(li[i], False)
  for i in range(n):
    GPIO.output(li[i], True)
   
def RGB(x,y):
  GPIO.output(16, x)
  GPIO.output(20, y)
  GPIO.output(21, False)

# GPIO_sensor
def gpio_set():
  GPIO.setmode(GPIO.BCM)

  GPIO.setup(18,GPIO.IN)
  GPIO.setup(26,GPIO.OUT)
  GPIO.setup(19,GPIO.OUT)
  GPIO.setup(13,GPIO.OUT)
  GPIO.setup(10,GPIO.OUT)
  GPIO.setup(17,GPIO.OUT)
  GPIO.setup(12,GPIO.OUT)
  GPIO.setup(16,GPIO.OUT)
  GPIO.setup(20,GPIO.OUT)
  GPIO.setup(21,GPIO.OUT)

  

# connect flask_db
def connect_db():
  conn = sqlite3.connect('studyPi.db')
  c = conn.cursor()
  c.execute("select * from users")
  db_list = c.fetchone()
  return db_list

# if __name__ == '__main__':
def sensor_on():
  start_time = None
  array = [0]*7
  gpio_set()
  while True:
    db_list = connect_db()
    if db_list is None:
      LED(0)
      RGB(False,False)
      GPIO.cleanup()
      break
    for i in range(7):
      array[i] = GPIO.input(18)
      time.sleep(1)
    if array[0] == GPIO.HIGH or array[1] == GPIO.HIGH or array[2] == GPIO.HIGH or  array[3] == GPIO.HIGH or  array[4] == GPIO.HIGH or array[5] == GPIO.HIGH or array[6] == GPIO.HIGH:
      if start_time is None:
        start_time = datetime.now()
      measure_time = datetime.now()
      medium_time = measure_time - start_time
      medium_second = medium_time.total_seconds()
      if medium_second <= 9:
        LED(6)
        RGB(False,True)
      elif medium_second >9 and medium_second <= 18:
        LED(5)
        RGB(False,True)
      elif medium_second >18 and medium_second <= 27:
        LED(4)
        RGB(False,True)
      elif medium_second >27 and medium_second <= 36:
        LED(3)
        RGB(False,True)
      elif medium_second >36 and medium_second <= 45:
        LED(2)
        RGB(False,True)
      elif medium_second >45 and medium_second <= 54:
        LED(1)
        RGB(False,True)
      elif medium_second >54:
        LED(0)
        RGB(False,True)
      time.sleep(3)
    else:
      if start_time is None:
        LED(0)
        RGB(True,False)
        time.sleep(3)
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
        LED(0)
        RGB(True,False)
        time.sleep(3)
