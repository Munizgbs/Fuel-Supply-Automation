from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone

db = create_engine("sqlite:///bank.db")

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True)
    cashback = Column(Float, default=0.0)
    password = Column(String)
    admin = Column(Boolean, default=False)


    refuels = relationship("Refuel", back_populates="user")

    def __init__(self, name, email, password, administrator=False):
        self.name = name
        self.email = email
        self.password = password
        self.administrator = administrator

class Refuel(Base):
    __tablename__ = "refuels"

    id_request = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("users.id"))
    fuel_type = Column(String, default="UNKNOWN")
    status = Column(String, default="PENDING")
    bonus = Column(Float, default=0.0)
    liters = Column(Float, default=0.0)
    value = Column(Float, default=0.0)
    date = Column(DateTime, datetime.now(timezone.utc))

    user = relationship("User", back_populates="refuels")

    def __init__(self, id_user, fuel_type="UNKNOWN", status="PENDING", liters=0.0):
        self.id_user = id_user
        self.fuel_type = fuel_type.upper().strip()
        self.status = status
        self.liters = liters

    def price(self):
        FUEL_PRICES = {
            "GASOLINE": 6.30,
            "DIESEL": 6.08,
            "ETHANOL": 4.63
        }

        if self.fuel_type in FUEL_PRICES:
            self.value = FUEL_PRICES[self.fuel_type] * self.liters
            self.bonus = self.value * 0.05
        else:
            raise ValueError("That type of fuel is not provided by the gas station.")
            