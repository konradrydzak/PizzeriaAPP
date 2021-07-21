from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class Menu(Base):
    __tablename__ = "menu"

    MenuID = Column(Integer, primary_key=True, index=True)
    Category = Column(String)
    Name = Column(String)
    Price = Column(Float)

    ordereditems = relationship("OrderedItems", back_populates="menu", cascade="all, delete")


class Orders(Base):
    __tablename__ = "orders"

    OrderID = Column(Integer, primary_key=True, index=True)
    TotalPrice = Column(Float)
    Comments = Column(String)
    Email = Column(String)

    ordereditems = relationship("OrderedItems", back_populates="orders", cascade="all, delete")


class OrderedItems(Base):
    __tablename__ = "ordereditems"

    OrderedItemID = Column(Integer, primary_key=True, index=True)
    MenuID = Column(Integer, ForeignKey("menu.MenuID"))
    OrderID = Column(Integer, ForeignKey("orders.OrderID"))
    Quantity = Column(Integer)
    UnitPrice = Column(Float)

    menu = relationship("Menu", back_populates="ordereditems")
    orders = relationship("Orders", back_populates="ordereditems")
