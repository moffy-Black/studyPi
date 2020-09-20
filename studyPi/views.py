from flask import Flask, request, jsonify, render_template, redirect, url_for, session, Response
from studyPi import app,db
import pyrebase
import json
from datetime import datetime

import RPi.GPIO as GPIO

from studyPi.models import User
from studyPi.camera import Camera

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

@app.route("/stream")
def stream():
  return render_template("stream.html")

def gen(camera):
  while True:
    frame = camera.get_frame()
    if frame is not None:
      yield (b"--frame\r\n"
      b"Content-Type: image/jpeg\r\n\r\n" + frame.tobytes() + b"\r\n")
    else:
      print("frame is None")

@app.route("/video_feed")
def video_feed():
  return Response(gen(Camera()),
  mimetype="multipart/x-mixed-replace; boundary=frame")