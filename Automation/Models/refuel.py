from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from Database.base import Base

class Refuel(Base):
    __tablename__ = "refuels"

    id_request = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("users.id"))
    fuel_type = Column(String, default="PENDING")
    status = Column(String, default="PENDING")
    bonus = Column(Float, default=0.0)
    additional_percentage = Column(Float, default=0.00)
    liters = Column(Float, default=0.0)
    value = Column(Float, default=0.0)
    date = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="refuels")
    payment = relationship("Payment", back_populates="refuels")
    promotion = relationship("Promotion", back_populates="refuels")

    def __init__(self, id_user, fuel_type="PENDING", status="PENDING", liters=0.0, additional_percentage=0.00):
        self.id_user = id_user
        self.fuel_type = fuel_type.upper().strip()
        self.status = status
        self.liters = liters
        self.additional_percentage = additional_percentage

    def price(self):
        FUEL_PRICES = {
            "GASOLINE": 6.30,
            "DIESEL": 6.08,
            "ETHANOL": 4.63
        }

        if self.fuel_type in FUEL_PRICES:
            self.value = ((FUEL_PRICES[self.fuel_type] * self.liters) * self.promotion) / 100
            self.bonus = self.value * self.additional_percentage
        else:
            raise ValueError("That type of fuel is not provided by the gas station.")