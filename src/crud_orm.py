import re

from fastapi import HTTPException
from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from src import models
from src import schemas

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


# MENU


def get_all_menu(db: Session):
    return db.query(models.Menu).order_by(models.Menu.MenuID.asc()).all()


def get_menu_items_by_name(db: Session, name: str):
    return db.query(models.Menu).filter(models.Menu.Name.ilike(f'%{name}%')).all()


def get_menu_items_by_category(db: Session, category: str):
    return db.query(models.Menu).filter(models.Menu.Category.ilike(category)).all()


def get_menu_item_by_id(db: Session, menu_id: int):
    return db.query(models.Menu).filter(models.Menu.MenuID == menu_id).first()


def add_item_to_menu(db: Session, item: schemas.AddItem):
    db_item = models.Menu(**item.dict())
    db.add(db_item)
    db.commit()

    db.refresh(db_item)
    return db_item


def edit_item_in_menu(db: Session, menu_id: int, item: schemas.EditItem):
    db_item = db.query(models.Menu).get(menu_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for var, value in vars(item).items():
        setattr(db_item, var, value) if value is not None else None  # Sets an attribute if it's provided
    db.commit()

    db.refresh(db_item)
    return db_item


def del_item_from_menu(db: Session, menu_id: int):
    db_item = db.query(models.Menu).filter(models.Menu.MenuID == menu_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()


# ORDERS


def get_all_orders(db: Session):
    return db.query(models.Orders).order_by(models.Orders.OrderID.asc()).all()


def get_orders_by_email(db: Session, email: str):
    return db.query(models.Orders).filter(models.Orders.Email.ilike(f'%{email}%')).all()


def get_order_by_id(db: Session, order_id: int):
    return db.query(models.Orders).filter(models.Orders.OrderID == order_id).first()


def add_order(db: Session, order: schemas.AddOrder):
    db_order = models.Orders(Comments=order.Comments, Email=order.Email, TotalPrice=0)
    if db_order.Email is not None:
        if not EMAIL_REGEX.match(db_order.Email):
            raise HTTPException(status_code=400, detail="Email is invalid")
    db.add(db_order)
    db.commit()

    # Add initial ordered items in OrderedItems
    if order.OrderedItems is not None:
        for ordereditem in order.OrderedItems:
            db_ordereditem_to_check = db.query(models.Menu).get(ordereditem.MenuID)
            if db_ordereditem_to_check is None:
                raise HTTPException(status_code=404, detail="Item not found")

            db_ordereditem = models.OrderedItems(OrderID=db_order.OrderID, MenuID=ordereditem.MenuID,
                                                 Quantity=ordereditem.Quantity,
                                                 UnitPrice=db.query(models.Menu).filter(
                                                     models.Menu.MenuID == ordereditem.MenuID).first().Price)
            db.add(db_ordereditem)
            db.commit()

    db.refresh(db_order)
    return db_order


def edit_order_in_orders(db: Session, order_id: int, order: schemas.EditOrder):
    db_order = db.query(models.Orders).get(order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for var, value in vars(order).items():
        if var == "Email" and value is not None:
            if db_order.Email is not None:
                if not EMAIL_REGEX.match(value):
                    raise HTTPException(status_code=400, detail="Email is invalid")
        setattr(db_order, var, value) if value is not None else None  # Sets an attribute if it's provided
    db.commit()

    db.refresh(db_order)
    return db_order


def del_order_from_orders(db: Session, order_id: int):
    db_order = db.query(models.Orders).filter(models.Orders.OrderID == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_order)
    db.commit()


# ORDEREDITEMS


def get_all_ordereditems(db: Session):
    return db.query(models.OrderedItems).order_by(models.OrderedItems.OrderedItemID.asc()).all()


def get_ordereditem_by_ordered_item_id(db: Session, ordered_item_id: int):
    return db.query(models.OrderedItems).filter(models.OrderedItems.OrderedItemID == ordered_item_id).first()


def get_ordereditems_by_order_id(db: Session, order_id: int):
    return db.query(models.OrderedItems).filter(models.OrderedItems.OrderID == order_id).all()


def get_ordereditems_by_menu_id(db: Session, menu_id: int):
    return db.query(models.OrderedItems).filter(models.OrderedItems.MenuID == menu_id).all()


def add_ordereditem_to_ordereditems(db: Session, ordereditem: schemas.AddOrderedItem):
    db_ordereditem_to_check = db.query(models.Menu).get(ordereditem.MenuID)
    if db_ordereditem_to_check is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_ordereditem_to_check = db.query(models.Orders).get(ordereditem.OrderID)
    if db_ordereditem_to_check is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db_ordereditem = models.OrderedItems(**ordereditem.dict(),
                                         UnitPrice=db.query(models.Menu).filter(
                                             models.Menu.MenuID == ordereditem.MenuID).first().Price)

    db.add(db_ordereditem)
    db.commit()

    db.refresh(db_ordereditem)
    return db_ordereditem


def edit_data_in_ordereditem(db: Session, ordered_item_id: int, ordereditem: schemas.EditOrderedItem):
    db_ordereditem = db.query(models.OrderedItems).get(ordered_item_id)
    if db_ordereditem is None:
        raise HTTPException(status_code=404, detail="Item not found")

    if ordereditem.MenuID is not None:
        db_ordereditem_to_check = db.query(models.Menu).get(ordereditem.MenuID)
        if db_ordereditem_to_check is None:
            raise HTTPException(status_code=404, detail="Item not found")
    if ordereditem.OrderID is not None:
        db_ordereditem_to_check = db.query(models.Orders).get(ordereditem.OrderID)
        if db_ordereditem_to_check is None:
            raise HTTPException(status_code=404, detail="Item not found")

    for var, value in vars(ordereditem).items():
        setattr(db_ordereditem, var, value) if value is not None else None  # Sets an attribute if it's provided
    # If price was not set manually, prepare UnitPrice value from Menu
    if ordereditem.UnitPrice is None:
        db_ordereditem.UnitPrice = db.query(models.Menu).filter(
            models.Menu.MenuID == db_ordereditem.MenuID).first().Price

    db.commit()

    # Set TotalPrice in Order to 0
    db_order = db.query(models.Orders).filter(
        models.Orders.OrderID == db_ordereditem.OrderID).first()
    db_order.TotalPrice = 0

    # For each Item associated to Order add the Price * Quantity
    db_items_in_order = db.query(models.OrderedItems).filter(
        models.OrderedItems.OrderID == db_ordereditem.OrderID).all()
    if db_items_in_order is not None:
        for item in db_items_in_order:
            db_order.TotalPrice += item.UnitPrice * item.Quantity

    db.commit()

    db.refresh(db_ordereditem)
    return db_ordereditem


def del_ordereditem_from_ordereditems(db: Session, ordered_item_id: int):
    db_ordereditem = db.query(models.OrderedItems).filter(models.OrderedItems.OrderedItemID == ordered_item_id).first()
    if db_ordereditem is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_ordereditem)
    db.commit()


# TRIGGERS


def change_totalprice_value(connection, target, should_add):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    db = SessionLocal()
    db_ordereditem = target

    db_order = db.query(models.Orders).filter(
        models.Orders.OrderID == db_ordereditem.OrderID).first()
    if should_add:
        db_order.TotalPrice += db_ordereditem.UnitPrice * db_ordereditem.Quantity
    else:
        db_order.TotalPrice -= db_ordereditem.UnitPrice * db_ordereditem.Quantity

    db.commit()


@event.listens_for(models.OrderedItems, 'after_insert')
def change_totalprice_after_insert(_, connection, target):
    change_totalprice_value(connection, target, should_add=True)


@event.listens_for(models.OrderedItems, 'before_delete')
def change_totalprice_before_delete(_, connection, target):
    change_totalprice_value(connection, target, should_add=False)
