from sqlalchemy import create_engine
from Database.base import Base

db = create_engine("sqlite:///bank.db")