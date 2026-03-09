from sqlalchemy import Column, String, Integer, Boolean, Float
from sqlalchemy.orm import relationship
from Database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True)
    cashback = Column(Float, default=0.0)
    password = Column(String)
    admin = Column(Boolean, default=False)

    refuel = relationship("Refuel", back_populates="users")
    payment = relationship("Payment", back_populates="users")

    def __init__(self, name, email, password, administrator=False):
        self.name = name
        self.email = email
        self.password = password
        self.administrator = administrator