from db import session
from models import User
from sqlalchemy.exc import SQLAlchemyError


def insert_data(local_id, name):
  # --- データの挿入 ---
  try:
    user = User(
        local_id=local_id,
        name=name
    )
    session.add(user)
    session.commit()
  except SQLAlchemyError as e:
    print(e)
    session.rollback()
  except Exception as e:
    session.rollback()
  finally:
    session.close()

def remove_data():
  # --- データを取り除く ---
  try:
    users = session.query(User).all()
    user = users[0]
    session.delete(user)
    session.commit()
  except SQLAlchemyError:
    session.rollback()
  except Exception as e:
    session.rollback()
  finally:
    session.close()