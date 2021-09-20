from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class MenuItems(Base):
    __tablename__ = "menu_items"

    menu_id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    name = Column(String)
    price = Column(Float)

    ordered_items = relationship("OrderedItems", back_populates="menu_items", cascade="all, delete")


class Orders(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    total_price = Column(Float)
    comments = Column(String)
    email = Column(String)

    ordered_items = relationship("OrderedItems", back_populates="orders", cascade="all, delete")


class OrderedItems(Base):
    __tablename__ = "ordered_items"

    ordered_item_id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey("menu_items.menu_id"))
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    quantity = Column(Integer)
    unit_price = Column(Float)

    menu_items = relationship("MenuItems", back_populates="ordered_items")
    orders = relationship("Orders", back_populates="ordered_items")
