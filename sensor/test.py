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

def LED(a,b,c,d,e,f,x,y,z):
   GPIO.output(yellow, a)
   GPIO.output(red1, b)
   GPIO.output(red2, c)
   GPIO.output(red3, d)
   GPIO.output(red4, e)
   GPIO.output(red5, f)
   GPIO.output(red_Pin, x)
   GPIO.output(green_Pin, y)
   GPIO.output(blue_Pin, z)

# GPIO_sensor
GPIO.setmode(GPIO.BCM)

GPIO_PIN = 18
yellow = 26
red1 = 19
red2 = 13
red3 = 10
red4 = 17
red5 = 12
red_Pin = 16
green_Pin = 20
blue_Pin = 21

GPIO.setup(GPIO_PIN,GPIO.IN)
GPIO.setup(yellow,GPIO.OUT)
GPIO.setup(red1,GPIO.OUT)
GPIO.setup(red2,GPIO.OUT)
GPIO.setup(red3,GPIO.OUT)
GPIO.setup(red4,GPIO.OUT)
GPIO.setup(red5,GPIO.OUT)
GPIO.setup(red_Pin,GPIO.OUT)
GPIO.setup(green_Pin,GPIO.OUT)
GPIO.setup(blue_Pin,GPIO.OUT)

# connect flask_db
conn = sqlite3.connect('studyPi/studyPi.db')
c = conn.cursor()
c.execute("select * from users")

# ardino settings
# ser = serial.Serial('/dev/ttyACM0', 9600)

# for time_measure value
start_time = None
array = [0]*7

if __name__ == '__main__':
  while True:
    db_list = c.fetchone()
    if db_list is None:
      GPIO.cleanup()
      break
    for i in range(5):
      array[i] = GPIO.input(GPIO_PIN)
      time.sleep(1)
    if array[0] == GPIO.HIGH or array[1] == GPIO.HIGH or array[2] == GPIO.HIGH or  array[3] == GPIO.HIGH or  array[4] == GPIO.HIGH or array[5] == GPIO.HIGH or array[6] == GPIO.HIGH:
      if start_time is None:
        start_time = datetime.now()
      measure_time = datetime.now()
      medium_time = measure_time - start_time
      medium_second = medium_time.total_seconds()
      if medium_second <= 9:
        # ser.write(str.encode('g'))
        LED(True,True,True,True,True,True,False,True,False)
      elif medium_second >9 and medium_second <= 18:
        # ser.write(str.encode('h'))
        LED(True,True,True,True,True,False,False,True,False)
      elif medium_second >18 and medium_second <= 27:
        # ser.write(str.encode('i'))
        LED(True,True,True,True,False,False,False,True,False)
      elif medium_second >27 and medium_second <= 36:
        # ser.write(str.encode('j'))
        LED(True,True,True,False,False,False,False,True,False)
      elif medium_second >36 and medium_second <= 45:
        # ser.write(str.encode('k'))
        LED(True,True,False,False,False,False,False,True,False)
      elif medium_second >45 and medium_second <= 54:
        # ser.write(str.encode('l'))
        LED(True,False,False,False,False,False,False,True,False)
      elif medium_second >54:
        # ser.write(str.encode('m'))
        LED(False,False,False,False,False,False,False,True,False)
      time.sleep(5)
    else:
      if start_time is None:
        LED(False,False,False,False,False,False,True,False,False)
        time.sleep(5)
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
        LED(False,False,False,False,False,False,True,False,False)
        time.sleep(5)
