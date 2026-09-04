from content_api.extensions import db
from sqlalchemy import select

def ping() -> bool:
    return True

def db_check():
        db.session.execute(select(1))
