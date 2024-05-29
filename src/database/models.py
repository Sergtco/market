from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    password = Column(String)
    transactions = relationship("Transaction", back_populates="owner")

    def count_stocks(self):
        curr_stocks = {}
        for trans in self.transactions:
            amount = trans.amount
            if trans.is_offer:
                amount *= -1
            if trans.stock.name not in curr_stocks:
                curr_stocks[trans.stock.name] = amount
            else:
                curr_stocks[trans.stock.name] += amount
        return curr_stocks


class Stock(Base):
    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    amount = Column(Integer)
    max_amount = Column(Integer)
    transactions = relationship("Transaction", back_populates="stock")


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    is_offer = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id"))
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    amount = Column(Integer)
    price = Column(Float)
    owner = relationship("User", back_populates="transactions")
    stock = relationship("Stock", back_populates="transactions")
