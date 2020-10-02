import responder
import os
import pyrebase
import json
import sqlite3

from store import insert_data, remove_data
from sensor import sensor_on

with open(("firebaseConfig.json")) as f:
    firebaseConfig = json.loads(f.read())
firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()

api = responder.API(
  templates_dir='templates',
  static_dir='static',
  static_route='/static',
  secret_key=os.urandom(24)
)

@api.route('/')
async def index(req, resp):
  displayName = req.session.get('displayName')
  if not displayName:
    api.redirect(resp,'/login')
  @api.background.task
  def sensor():
    sensor_on()
    print("end")
  sensor()
  resp.content = api.template('index.html',name=displayName)

@api.route('/login')
async def login(req, resp):
  if req.method == 'get':
    remove_data()
    resp.content = api.template('login.html',msg="")
    return
  else:
    data = await req.media()
    email = data.get('email')
    password = data.get('password')
    try:
      # ---Firebase's Function---
      user = auth.sign_in_with_email_and_password(email, password)
      localId=user["localId"]
      name=user["displayName"]
      insert_data(localId, name)
      resp.session['displayName']=name
      api.redirect(resp, '/')
    except:
      resp.content = api.template('login.html',msg="メールアドレスまたはパスワードが間違っています。")

if __name__ == "__main__":
  api.run(address="0.0.0.0",port=5050, debug=True)