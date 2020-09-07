from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from studyPi import app,db
import pyrebase
import json

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
      email=email,
      password=password
    )
    db.session.add(ur)
    db.session.commit()
    return redirect(url_for('index'))
  except:
    return render_template("login.html", msg="メールアドレスまたはパスワードが間違っています。")

@app.route("/", methods=['GET'])
def index():
  # usr = User.query.get(1).email
  usr = User.query.all()
  if not usr:
    return redirect(url_for('login'))
  return render_template("index.html", usr=usr[0])

@app.route('/logout')
def logout():
  usr = User.query.get(1).email
  obj = User.query.filter_by(email='{}'.format(usr)).one()
  db.session.delete(obj)
  db.session.commit()
  return redirect(url_for('login'))