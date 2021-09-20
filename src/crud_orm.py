import re

from fastapi import HTTPException
from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from src import models
from src import schemas

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


# MENU


def get_all_menu_items(db: Session):
    return db.query(models.MenuItems).order_by(models.MenuItems.id.asc()).all()


def get_menu_items_by_name(db: Session, name: str):
    return db.query(models.MenuItems).filter(models.MenuItems.name.ilike(f'%{name}%')).all()


def get_menu_items_by_category(db: Session, category: str):
    return db.query(models.MenuItems).filter(models.MenuItems.category.ilike(category)).all()


def get_menu_item_by_id(db: Session, id: int):
    return db.query(models.MenuItems).filter(models.MenuItems.id == id).first()


def add_to_menu_items(db: Session, item: schemas.AddItem):
    db_item = models.MenuItems(**item.dict())
    db.add(db_item)
    db.commit()

    db.refresh(db_item)
    return db_item


def edit_item_in_menu_items(db: Session, id: int, item: schemas.EditItem):
    db_item = db.query(models.MenuItems).get(id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for var, value in vars(item).items():
        setattr(db_item, var, value) if value is not None else None  # Sets an attribute if it's provided
    db.commit()

    db.refresh(db_item)
    return db_item


def del_item_from_menu_items(db: Session, id: int):
    db_item = db.query(models.MenuItems).filter(models.MenuItems.id == id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()


# ORDERS


def get_all_orders(db: Session):
    return db.query(models.Orders).order_by(models.Orders.id.asc()).all()


def get_orders_by_email(db: Session, email: str):
    return db.query(models.Orders).filter(models.Orders.email.ilike(f'%{email}%')).all()


def get_order_by_id(db: Session, id: int):
    return db.query(models.Orders).filter(models.Orders.id == id).first()


def add_to_orders(db: Session, order: schemas.AddOrder):
    db_order = models.Orders(comments=order.comments, email=order.email, total_price=0)
    if db_order.email is not None:
        if not EMAIL_REGEX.match(db_order.email):
            raise HTTPException(status_code=400, detail="email is invalid")
    db.add(db_order)
    db.commit()

    # Add initial ordered items in OrderedItems
    if order.ordered_items is not None:
        for ordered_item in order.ordered_items:
            db_ordered_item_to_check = db.query(models.MenuItems).get(ordered_item.menu_item_id)
            if db_ordered_item_to_check is None:
                raise HTTPException(status_code=404, detail="Item not found")

            db_ordered_item = models.OrderedItems(order_id=db_order.id, menu_item_id=ordered_item.menu_item_id,
                                                  quantity=ordered_item.quantity,
                                                  unit_price=db.query(models.MenuItems).filter(
                                                      models.MenuItems.id == ordered_item.menu_item_id).first().price)
            db.add(db_ordered_item)
            db.commit()

    db.refresh(db_order)
    return db_order


def edit_item_in_orders(db: Session, id: int, order: schemas.EditOrder):
    db_order = db.query(models.Orders).get(id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for var, value in vars(order).items():
        if var == "email" and value is not None:
            if db_order.email is not None:
                if not EMAIL_REGEX.match(value):
                    raise HTTPException(status_code=400, detail="email is invalid")
        setattr(db_order, var, value) if value is not None else None  # Sets an attribute if it's provided
    db.commit()

    db.refresh(db_order)
    return db_order


def del_item_from_orders(db: Session, id: int):
    db_order = db.query(models.Orders).filter(models.Orders.id == id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_order)
    db.commit()


# ORDEREDITEMS


def get_all_ordered_items(db: Session):
    return db.query(models.OrderedItems).order_by(models.OrderedItems.id.asc()).all()


def get_ordered_item_by_id(db: Session, id: int):
    return db.query(models.OrderedItems).filter(models.OrderedItems.id == id).first()


def get_ordered_items_by_menu_item_id(db: Session, menu_item_id: int):
    db_ordered_items = db.query(models.OrderedItems).filter(models.OrderedItems.menu_item_id == menu_item_id).all()
    if db_ordered_items:
        return db_ordered_items
    else:
        raise HTTPException(status_code=404, detail="Item not found")


def get_ordered_items_by_order_id(db: Session, order_id: int):
    db_ordered_items = db.query(models.OrderedItems).filter(models.OrderedItems.order_id == order_id).all()
    if db_ordered_items:
        return db_ordered_items
    else:
        raise HTTPException(status_code=404, detail="Item not found")


def add_to_ordered_items(db: Session, ordered_item: schemas.AddOrderedItem):
    db_ordered_item_to_check = db.query(models.MenuItems).get(ordered_item.menu_item_id)
    if db_ordered_item_to_check is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_ordered_item_to_check = db.query(models.Orders).get(ordered_item.order_id)
    if db_ordered_item_to_check is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db_ordered_item = models.OrderedItems(**ordered_item.dict(),
                                          unit_price=db.query(models.MenuItems).filter(
                                              models.MenuItems.id == ordered_item.menu_item_id).first().price)

    db.add(db_ordered_item)
    db.commit()

    db.refresh(db_ordered_item)
    return db_ordered_item


def edit_item_in_ordered_items(db: Session, id: int, ordered_item: schemas.EditOrderedItem):
    db_ordered_item = db.query(models.OrderedItems).get(id)
    if db_ordered_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    if ordered_item.menu_item_id is not None:
        db_ordered_item_to_check = db.query(models.MenuItems).get(ordered_item.menu_item_id)
        if db_ordered_item_to_check is None:
            raise HTTPException(status_code=404, detail="Item not found")
    if ordered_item.order_id is not None:
        db_ordered_item_to_check = db.query(models.Orders).get(ordered_item.order_id)
        if db_ordered_item_to_check is None:
            raise HTTPException(status_code=404, detail="Item not found")

    for var, value in vars(ordered_item).items():
        setattr(db_ordered_item, var, value) if value is not None else None  # Sets an attribute if it's provided
    # If price was not set manually, prepare unit_price value from MenuItems
    if ordered_item.unit_price is None:
        db_ordered_item.unit_price = db.query(models.MenuItems).filter(
            models.MenuItems.id == db_ordered_item.menu_item_id).first().price

    db.commit()

    # Set total_price in Order to 0
    db_order = db.query(models.Orders).filter(
        models.Orders.id == db_ordered_item.order_id).first()
    db_order.total_price = 0

    # For each Item associated to Order add the price * quantity
    db_items_in_order = db.query(models.OrderedItems).filter(
        models.OrderedItems.id == db_ordered_item.id).all()
    if db_items_in_order is not None:
        for item in db_items_in_order:
            db_order.total_price += item.unit_price * item.quantity

    db.commit()

    db.refresh(db_ordered_item)
    return db_ordered_item


def del_item_from_ordered_items(db: Session, id: int):
    db_ordered_item = db.query(models.OrderedItems).filter(
        models.OrderedItems.id == id).first()
    if db_ordered_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_ordered_item)
    db.commit()


# TRIGGERS


def change_total_price_value(connection, target, should_add):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    db = SessionLocal()
    db_ordered_item = target

    db_order = db.query(models.Orders).filter(
        models.Orders.id == db_ordered_item.order_id).first()
    if should_add:
        db_order.total_price += db_ordered_item.unit_price * db_ordered_item.quantity
    else:
        db_order.total_price -= db_ordered_item.unit_price * db_ordered_item.quantity
    db.commit()


@event.listens_for(models.OrderedItems, 'after_insert')
def change_total_price_after_insert(_, connection, target):
    change_total_price_value(connection, target, should_add=True)


@event.listens_for(models.OrderedItems, 'before_delete')
def change_total_price_before_delete(_, connection, target):
    change_total_price_value(connection, target, should_add=False)
