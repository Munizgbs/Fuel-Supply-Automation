from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

db = create_engine("sqlite:///bank.db")

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    email = Column("email", String, unique=True)
    name = Column("name", String)
    password = Column("password", String)
    cashback = Column("cashback", Float)
    administrator = Column("administrator?", Boolean)

    def __init__(self, email, name, password, administrator=False):
        self.email = email
        self.name = name
        self.password = password
        self.administrator = administrator

class Service(Base):
    __tablename__ = "service"

    id_service = Column("id_service", Integer, primary_key=True, autoincrement=True)
    id_user = Column("id", Integer, ForeignKey("users.id"))
    fuel_type = Column("fuel_type", String)
    liters = Column("liters", Integer)
    value = Column("value", Float)
    date = Column("date", DateTime, default=datetime.utcnow)
