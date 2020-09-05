from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from studyPi import app,db
import pyrebase
import json

from studyPi.models import User

with open("firebaseConfig.json") as f:
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
    session['usr'] = email

    # ---studyPi's Function---
    # ur = User(
    #   email=email,
    #   password=password
    # )
    # db.session.add(ur)
    # db.session.commit()
    return redirect(url_for('index'))
  except:
    return render_template("login.html", msg="メールアドレスまたはパスワードが間違っています。")

@app.route("/", methods=['GET'])
def index():
  usr = session.get('usr')
  if usr == None:
    return redirect(url_for('login'))
  return render_template("index.html", usr=usr)

@app.route('/logout')
def logout():
  del session['usr']
  return redirect(url_for('login'))