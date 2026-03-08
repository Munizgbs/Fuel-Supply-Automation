from pydantic import BaseModel
from typing import Optional

class ServiceSchema(BaseModel):
    fuel_type: str
    liters: float

    class Config():
        from_attributes = True