from fastapi import APIRouter, Depends, HTTPException
from schemas import UserSchemas
from sqlalchemy.orm import Session
from dependencies import UseSession
from models import User

auth_router = APIRouter(prefix="/authenticator", tags=["authenticator"])

def authenticate(email, password, session):
    user = session.query(User).filter(User.email=email).first()
    if not user:
        return False
    else:
        return user


@auth_router.post("/register")
async def register(user_schema: UserSchemas, session: Session=Depends(UseSession)):
    user = authenticate(user_schema.email)
    if user:
        raise HTTPException(status_Code=400, detail="This email address is already in use.")
    else:
        new_user = User(user_schema.name, user_schema.email, user_schema.password, user_schema.administrator)
        session.add(new_user)
        session.commit()
        return HTTPException(status_code=200, detail="Your registration has been completed.")
    