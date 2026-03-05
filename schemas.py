from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id: Optional[int] = None
    name: Optional [str]
    email: str
    password: str
    admin: Optional [bool]

    class Config():
        from_attributes = True

class ServiceSchema(BaseModel):
    fuel_type: str
    user_id: int
    liters: float
    value: float

    class Config():
        from_attributes = True