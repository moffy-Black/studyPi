from studyPi import db

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  local_id = db.Column(db.String(100), nullable=False)
  name = db.Column(db.String(100), nullable=False)

  def __repr__(self):
    return '<User id={id} name={name!r}>'.format(
      id=self.id, name=self.name)
def init():
  db.create_all()