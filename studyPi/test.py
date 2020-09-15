from datetime import datetime
import time
import RPi.GPIO as GPIO
import pyrebase
import json

from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from studyPi import app,db
from studyPi.models import User

with open("./firebaseConfig.json") as f:
    firebaseConfig = json.loads(f.read())
firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

GPIO_PIN = 18
catch = datetime.now()
release = datetime.now()
T = 0
d = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN,GPIO.IN)

if __name__ == '__main__':
  try:
    
    while True:
      if(GPIO.input(GPIO_PIN) == GPIO.HIGH):
        catch = datetime.now()
        T += d
        d = 0
      else:
        release = datetime.now()
        DELTA = release - catch
        d = DELTA.total_seconds()
        if d >= 20.0:
          break
  except KeyboardInterrupt:
    pass
    
  finally:
    s = T
    date = release.strftime('%Y-%m-%d')
    term = s // 60
    time = release.strftime('%H:%M')
    push_date = {
      "date": date,
      "term": term,
      "time": time
    }
    records = db.child("records").child("bz5pWlLkslU1TM7YReke8OSuxSM2").push(push_date)
    GPIO.cleanup()
    print(T)
