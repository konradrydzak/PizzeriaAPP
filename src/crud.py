from fastapi import HTTPException
from sqlalchemy.orm import Session

from src import models
from src import schemas


def get_menu_full(db: Session):
    return db.query(models.Menu).order_by(models.Menu.MenuID.asc()).all()


def get_menu_item_by_id(db: Session, menu_id: int):
    return db.query(models.Menu).filter(models.Menu.MenuID == menu_id).first()


def get_menu_items_by_name(db: Session, name: int):
    return db.query(models.Menu).filter(models.Menu.Name.ilike(f'%{name}%')).all()


def get_menu_items_by_category(db: Session, category: int):
    return db.query(models.Menu).filter(models.Menu.Category.ilike(category)).all()


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
