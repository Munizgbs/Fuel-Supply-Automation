from fastapi import APIRouter, Depends, HTTPException
from schemas import UserSchema
from sqlalchemy.orm import Session
from dependencies import use_session, verification
from main import bcrypt_context, ACCESS_TOKEN_EXPIRE, ALGORITHM, SECRET_KEY
from models import User
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/authenticator", tags=["authenticator"])

def create_token(user_id, time_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE)):
    expiration = datetime.now(timezone.utc) + timedelta(time_token)
    information = {"sub": str(User.id), "exp": expiration}
    encoded = jwt.encode(information, SECRET_KEY, ALGORITHM)
    return encoded


def authenticate(email, password, session):
    user = session.query(User).filter(User.email==email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, User.password):
        return False
    return user


@auth_router.post("/register")
async def register(user_schema: UserSchema, session: Session=Depends(use_session)):
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
async def login(user_schema: UserSchema, session: Session=Depends(use_session)):
    user = authenticate(user_schema.email, user_schema.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="The user was not found or the credentials are invalid.")
    else:
        access_token = create_token(User.id)
        refresh_token = create_token(User.id, time_token=timedelta(days=7))
        return {
            "acess_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
            }
    

@auth_router.post("/form")
async def form(form: OAuth2PasswordRequestForm=Depends(), session: Session=Depends(use_session)):
    user = authenticate(form.username, form.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="The user was not found or the credentials are invalid.")
    else:
        access_token = create_token(User.id)
        refresh_token = create_token(User.id, time_token=timedelta(days=7))
        return {
            "acess_token": access_token,
            "token_type": "Bearer"
            }

@auth_router.get("/refresh")
async def refresh(user: User=Depends(verification)):
    access_token = create_token()
    return {
            "acess_token": access_token,
            "token_type": "Bearer"
            }

#login -> email e senha -> token JWT