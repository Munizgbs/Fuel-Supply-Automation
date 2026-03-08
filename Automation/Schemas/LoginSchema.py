from pydantic import BaseModel
from typing import Optional

class LoginSchema(BaseModel):
    email: str
    password: str

    class Config():
        from_attributes =  True