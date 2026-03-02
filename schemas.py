from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    administrator: Optional[bool]

    class Config():
        from_attributes = True
