from sqlalchemy import Column, Integer, String, BigInteger
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True)
    balance = Column(Integer, default=0)
    invited_by = Column(BigInteger)
    successful_invites = Column(Integer, default=0)

class Settings(Base):
    __tablename__ = "settings"
    key = Column(String, primary_key=True)
    value = Column(String)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    amount = Column(Integer)
    status = Column(String)  # pending / paid / rejected
    receipt = Column(String)
