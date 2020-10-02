import os
from datetime import datetime

from db import Base
from db import engine

from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER

SQLITE3_NAME = "./studyPi.db"

class User(Base):
  __tablename__ = 'users'

  id = Column(
    INTEGER(unsigned=True),
    primary_key=True,
    autoincrement=True
  )
  local_id = Column(String(256))
  name = Column(String(256))
  def __repr__(self):
    return '<User id={id} name={name!r}>'.format(
      id=self.id, name=self.name)

if __name__ == "__main__":
  path = SQLITE3_NAME
  if not os.path.isfile(path):
    # テーブル作成
    Base.metadata.create_all(engine)