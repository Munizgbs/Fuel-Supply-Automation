from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE = int(os.getenv("ACCESS_TOKEN_EXPIRE"))

app = FastAPI()

Base.metadata.create_all(bind=db)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="authenticator/form")

from Routers.auth import auth_router
from Routers.user import user_router
from Routers.admin import admin_router

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)