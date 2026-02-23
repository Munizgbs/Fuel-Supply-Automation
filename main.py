from fastapi import FastAPI

app = FastAPI()


from auth_routes import auth_router
from user_routes import user_router
from admin_routes import admin_router

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)