from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

db = create_engine("sqlite:///bank.db")

Base = declarative_base()

Base.metadata.create_all(db)