from sqlalchemy.orm import sessionmaker, Session
from models import db, User
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_schema

def use_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verification(token: str=Depends(oauth2_schema), session: Session=Depends(use_session)):
    try:
        information = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = int(information.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Access Denied, check token validity.")
    if not User:
        raise HTTPException(status_code=401, detail="Access Denied")
    return User

