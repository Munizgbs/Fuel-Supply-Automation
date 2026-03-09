from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from Database.base import Base

class Promotion(Base):
    __tablename__ = "promotions"

    id_promotion = Column(Integer, primary_key=True, autoincrement=True)
    fuel_type = Column(String, ForeignKey("refuels.fuel_type"))
    discount = Column(Float, default=0.00)
    status = Column(String, default="PENDING")

    start = Column(DateTime)
    end = Column(DateTime)

    refuel = relationship("Refuel", back_populates="promotions")
    payment = relationship("Payment", back_populates="promotions")

    def __init__(self, discount=0.00, status="PENDING"):
        self.discount = discount
        self.status = status