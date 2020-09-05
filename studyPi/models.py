from studyPi import db

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(100), unique=True, nullable=False)
  password = db.Column(db.String(100), nullable=False)

  def __repr__(self):
    return '<User id={id} email={email!r}>'.format(
      id=self.id, email=self.email)
def init():
  db.create_all()