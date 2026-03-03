from fastapi import APIRouter, Depends, HTTPException
from schemas import UserSchema
from sqlalchemy.orm import Session
from dependencies import UseSession
from main import bcrypt_context
from models import User

auth_router = APIRouter(prefix="/authenticator", tags=["authenticator"])

def create_token():
    pass

def authenticate(email, password, session):
    user = session.query(User).filter(User.email==email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, User.password):
        return False
    return user


@auth_router.post("/register")
async def register(user_schema: UserSchema, session: Session=Depends(UseSession)):
    user = authenticate(user_schema.email)
    if user:
        raise HTTPException(status_code=400, detail="This email address is already in use.")
    else:
        encrypted_password = bcrypt_context.hash(user_schema.password)
        new_user = User(user_schema.name, user_schema.email, encrypted_password)
        session.add(new_user)
        session.commit()
        return {"message": "Your registration has been completed."}

@auth_router.post("/login")
async def login (user_schema: UserSchema, session: Session=Depends(UseSession)):
    
#login -> email e senha -> token JWT