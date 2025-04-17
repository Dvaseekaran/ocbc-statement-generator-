from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(String, index=True)
    date = Column(DateTime)
    amount = Column(Float)
    description = Column(String)
    merchant = Column(String)
    category = Column(String)