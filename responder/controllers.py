import responder
import os
import sqlite3

from firebase import auth
from store import insert_data, remove_data
from sensor import sensor

api = responder.API(
  templates_dir='templates',
  static_dir='static',
  static_route='/static',
  secret_key=os.urandom(24)
)

class IndexController:
  async def on_get(self, req, resp): #HTTP method get
    @api.background.task
    def sensor_on():
      sensor()
    displayName = req.session.get('displayName')
    if not displayName:
      api.redirect(resp,'/login')
    sensor_on()
    resp.content = api.template('index.html',name=displayName)

class LoginController:
  async def on_get(self, req, resp): #HTTP method get
    @api.background.task
    def process_remove_data():
      remove_data()
    process_remove_data()
    resp.content = api.template('login.html',msg="")

  async def on_post(self, req, resp): #HTTP method post
    @api.background.task
    def process_insert_data(localId, name):
      insert_data(localId, name)
    data = await req.media()
    email = data.get('email')
    password = data.get('password')
    try:
      # ---Firebase's Function---
      user = auth.sign_in_with_email_and_password(email, password)
      localId=user["localId"]
      name=user["displayName"]
      # -------------------------
      resp.session['displayName']=name
      process_insert_data(localId, name)
      api.redirect(resp, '/')
    except:
      resp.content = api.template('login.html',msg="メールアドレスまたはパスワードが間違っています。")