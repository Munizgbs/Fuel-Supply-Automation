from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id: Optional [int]
    name: Optional [str]
    email: str
    password: str
    admin: Optional [bool]

    class Config():
        from_attributes = True

class ServiceSchema(BaseModel):
    typee: str
    user_id = int
    liters: int

    class Config():
        from_attributes = True