from datetime import datetime
import RPi.GPIO as GPIO
import time
import sqlite3

from firebase import db

# LED ON or OFF
def LED(n):
  li = [26,19,13,10,17,12]
  [GPIO.output(i, False) for i in li]
  [GPIO.output(li[i], True) for i in range(n)]

# RGB ON or OFF
def RGB(x,y):
  GPIO.output(16, x)
  GPIO.output(20, y)
  GPIO.output(21, False)

# GPIOPIN set
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

# connect sqlite3
def connect_db():
  conn = sqlite3.connect('studyPi.db')
  c = conn.cursor()
  c.execute("select * from users")
  db_list = c.fetchone()
  return db_list

def calculate(x, y):
  delta_time = x - y
  delta_second = delta_time.total_seconds()
  return delta_second

# main function
def sensor():
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
      medium_second = calculate(measure_time, start_time)
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
        delta_second = calculate(finish_time, start_time)
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
        # records = db.child("records").child(user_id).push(push_date)
        start_time = None
        LED(0)
        RGB(True,False)
        time.sleep(53)
