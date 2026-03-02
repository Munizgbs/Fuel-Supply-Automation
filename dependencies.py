from sqlalchemy.orm import sessionmaker, Session
from models import db

def UseSession():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally
        session.close()