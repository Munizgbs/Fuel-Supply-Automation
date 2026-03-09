from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from Database.base import Base

class Payment(Base):
    __tablename__ = "payments"

    id_payment = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("users.id"))
    id_refuel = Column(Integer, ForeignKey("refuels.id_request"))

    method = Column(String, default="PENDING")
    total_value = Column(Float, ForeignKey("refuels.value"))
    date = Column(DateTime, default=datetime.now(timezone.utc))

    refuel = relationship("Refuel", back_populates="payments")
    user = relationship("User", back_populates="payments")
    promotion = relationship("Promotion", back_populates="payments")

    def __init__(self, method="PENDING"):
        self.method = method
