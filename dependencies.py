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
        information = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_user = int(information.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Access Denied, check token validity.")
    if not id_user:
        raise HTTPException(status_code=401, detail="Access Denied")
    user = session.query(User).filter(User.id == id_user).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def administrator(user: User=Depends(verification)):
    if not user.admin:
        raise HTTPException(status_code=401,detail="You are not authorized to perform this operation.")