from typing import Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.orm import Session

from src import config
from src import models
from src import schemas, crud_sql, crud_orm
from src.database import SessionLocal, engine

# SET ORM/SQL MODE TO USE
params = config.config()
USE_ORM = params["use_orm"]
if USE_ORM == "True":
    crud = crud_orm
else:
    crud = crud_sql  # Note: this mode does not use models.py file

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PizzeriaAPP",
    description="This is the auto docs webpage for the PizzeriaAPP API",
    version="1.0",
)

tags_metadata = [
    {
        "name": "menu_items",
    },
    {
        "name": "orders",
    },
    {
        "name": "ordered_items",
    },
]


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# MENU


# GET all menu items or some items from menu searched by name or by category
@app.get("/menu", tags=['menu_items'])
def read_menu_items(name: Optional[str] = None, category: Optional[str] = None, db: Session = Depends(get_db)):
    if name:
        menu = crud.get_menu_items_by_name(db=db, name=name)
    elif category:
        menu = crud.get_menu_items_by_category(db=db, category=category)
    else:
        menu = crud.get_all_menu_items(db=db)
    if not menu:
        raise HTTPException(status_code=404, detail="Item not found")
    return menu


# GET item from menu by _id
@app.get("/menu/{id}", tags=['menu_items'])
def read_menu_item_by_menu_id(id: int, db: Session = Depends(get_db)):
    menu_item = crud.get_menu_item_by_id(db=db, id=id)
    if menu_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return menu_item


# POST an item to menu
@app.post("/menu", status_code=201, tags=['menu_items'])
def post_to_menu_items(item: schemas.AddItem, db: Session = Depends(get_db)):
    return crud.add_to_menu_items(db=db, item=item)


# PATCH data in an item from menu
@app.patch("/menu/{id}", tags=['menu_items'])
def patch_data_in_menu_item(id: int, item: schemas.EditItem, db: Session = Depends(get_db)):
    return crud.edit_item_in_menu_items(db=db, id=id, item=item)


# DELETE item from menu
@app.delete("/menu/{id}", status_code=204, response_class=Response, tags=['menu_items'])
def del_item_from_menu_items(id: int, db: Session = Depends(get_db)):
    crud.del_item_from_menu_items(db=db, id=id)


# ORDERS


# GET all orders or some orders from orders searched by an email
@app.get("/orders", tags=['orders'])
def read_orders(email: Optional[str] = None, db: Session = Depends(get_db)):
    if email:
        orders = crud.get_orders_by_email(db=db, email=email)
    else:
        orders = crud.get_all_orders(db=db)
    if not orders:
        raise HTTPException(status_code=404, detail="Item not found")
    return orders


# GET order from orders by order_id
@app.get("/orders/{id}", tags=['orders'])
def read_order_by_order_id(id: int, db: Session = Depends(get_db)):
    order = crud.get_order_by_id(db=db, id=id)
    if order is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return order


# POST an order to orders
@app.post("/orders", status_code=201, tags=['orders'])
def post_to_orders(order: schemas.AddOrder, db: Session = Depends(get_db)):
    return crud.add_to_orders(db=db, order=order)


# PATCH data in an order from orders
@app.patch("/orders/{id}", tags=['orders'])
def patch_data_in_order(id: int, order: schemas.EditOrder, db: Session = Depends(get_db)):
    return crud.edit_item_in_orders(db=db, id=id, order=order)


# DELETE order from orders
@app.delete("/orders/{id}", status_code=204, response_class=Response, tags=['orders'])
def del_item_from_orders(id: int, db: Session = Depends(get_db)):
    crud.del_item_from_orders(db=db, id=id)


# ORDERED_ITEMS


# GET all ordered items from ordered_items
@app.get("/ordereditems", tags=['ordered_items'])
def read_ordered_items(db: Session = Depends(get_db)):
    ordered_items = crud.get_all_ordered_items(db=db)
    if not ordered_items:
        raise HTTPException(status_code=404, detail="Item not found")
    return ordered_items


# GET ordered item from ordereditems by ordered_item_id
@app.get("/ordereditems/{id}", tags=['ordered_items'])
def read_ordered_item_by_id(id: int, db: Session = Depends(get_db)):
    ordered_item = crud.get_ordered_item_by_id(db=db, id=id)
    if ordered_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return ordered_item


# GET ordered items from ordered_items by order_id
@app.get("/ordereditems/orderid/{order_id}", tags=['ordered_items'])
def read_ordered_items_by_order_id(order_id: int, db: Session = Depends(get_db)):
    ordereditems = crud.get_ordered_items_by_order_id(db=db, order_id=order_id)
    if ordereditems is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return ordereditems


# GET ordered items from ordered_items by menu_item_id
@app.get("/ordereditems/menuitemid/{menu_item_id}", tags=['ordered_items'])
def read_ordered_items_by_menu_item_id(menu_item_id: int, db: Session = Depends(get_db)):
    ordereditems = crud.get_ordered_items_by_menu_item_id(db=db, menu_item_id=menu_item_id)
    if ordereditems is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return ordereditems


# POST an ordered item to ordered_items
@app.post("/ordereditems", status_code=201, tags=['ordered_items'])
def post_to_ordered_items(ordered_item: schemas.AddOrderedItem, db: Session = Depends(get_db)):
    return crud.add_to_ordered_items(db=db, ordered_item=ordered_item)


# PATCH data in an ordered item from ordered_items
@app.patch("/ordereditems/{id}", tags=['ordered_items'])
def patch_data_in_ordered_item(id: int, ordered_item: schemas.EditOrderedItem,
                               db: Session = Depends(get_db)):
    return crud.edit_item_in_ordered_items(db=db, id=id, ordered_item=ordered_item)


# DELETE ordered item from ordered_items
@app.delete("/ordereditems/{id}", status_code=204, response_class=Response, tags=['ordered_items'])
def del_item_from_ordered_items(id: int, db: Session = Depends(get_db)):
    crud.del_item_from_ordered_items(db=db, id=id)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
