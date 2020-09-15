from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from studyPi import app,db
import pyrebase
import json
from datetime import datetime

import RPi.GPIO as GPIO

from studyPi.models import User

with open("studyPi/firebaseConfig.json") as f:
    firebaseConfig = json.loads(f.read())
firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return render_template("login.html",msg="")

  email = request.form['email']
  password = request.form['password']
  try:
    # ---Firebase's Function---
    user = auth.sign_in_with_email_and_password(email, password)
    # ---studyPi's Function---
    ur = User(
      local_id=user["localId"],
      name=user["displayName"]
    )
    db.session.add(ur)
    db.session.commit()
    return redirect(url_for('index'))
  except:
    return render_template("login.html", msg="メールアドレスまたはパスワードが間違っています。")

@app.route("/", methods=['GET'])
def index():
  usr = User.query.all()
  if not usr:
    return redirect(url_for('login'))
  return render_template("index.html", usr=usr[0])

@app.route('/logout')
def logout():
  usr = User.query.get(1).name
  obj = User.query.filter_by(name='{}'.format(usr)).one()
  db.session.delete(obj)
  db.session.commit()
  return redirect(url_for('login'))

@app.route('/study')
def study():
  time_measure()
  return redirect(url_for('logout'))

import time
def time_measure():
  database = firebase.database()
  
  GPIO_PIN = 18
  catch = datetime.now()
  release = datetime.now()
  T = 0
  d = 0

  GPIO.setmode(GPIO.BCM)
  GPIO.setup(GPIO_PIN,GPIO.IN)
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
    s = int(T)
    date = release.strftime('%Y-%m-%d')
    term = str(s // 60)
    Ntime = release.strftime('%H:%M')
    push_date = {
      "date": date,
      "term": term,
      "time": Ntime
    }
    records = database.child("records").child(User.query.get(1).local_id).push(push_date)
    GPIO.cleanup()
