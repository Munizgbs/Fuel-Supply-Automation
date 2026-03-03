from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    name: Optional [str]
    email: str
    password: str

    class Config():
        from_attributes = True

class ServiceSchema(BaseModel):
    typee: str
    user_id = int
    liters: int

    class Config():
        from_attributes = True