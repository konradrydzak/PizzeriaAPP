from typing import Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.orm import Session

from src import models
from src import schemas, crud
from src.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PizzeriaAPP",
    description="This is the auto docs webpage for the PizzeriaAPP API",
    version="1.0",
)

tags_metadata = [
    {
        "name": "menu",
    },
    {
        "name": "orders",
    },
    {
        "name": "ordereditems",
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


# GET Full menu or some items from menu searched by name or by category
@app.get("/menu", tags=['menu'])
def read_menu(name: Optional[str] = None, category: Optional[str] = None, db: Session = Depends(get_db)):
    if name:
        menu = crud.get_menu_items_by_name(db, name=name)
    elif category:
        menu = crud.get_menu_items_by_category(db, category=category)
    else:
        menu = crud.get_all_menu(db)
    if not menu:
        raise HTTPException(status_code=404, detail="Item not found")
    return menu


# GET item from menu by ID
@app.get("/menu/{menu_id}", tags=['menu'])
def read_menu_item_by_menu_id(menu_id: int, db: Session = Depends(get_db)):
    menu_item = crud.get_menu_item_by_id(db, menu_id=menu_id)
    if menu_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return menu_item


# POST an item to menu
@app.post("/menu", status_code=201, tags=['menu'])
def post_item_to_menu(item: schemas.AddItem, db: Session = Depends(get_db)):
    return crud.add_item_to_menu(db=db, item=item)


# PATCH data in an item from menu
@app.patch("/menu/{menu_id}", tags=['menu'])
def patch_data_in_item(menu_id: int, item: schemas.EditItem, db: Session = Depends(get_db)):
    return crud.edit_item_in_menu(db=db, menu_id=menu_id, item=item)


# DELETE item from menu
@app.delete("/menu/{menu_id}", status_code=204, response_class=Response, tags=['menu'])
def del_item_from_menu(menu_id: int, db: Session = Depends(get_db)):
    crud.del_item_from_menu(db=db, menu_id=menu_id)


# ORDERS


# GET All orders or some orders from orders searched by an email
@app.get("/orders", tags=['orders'])
def read_orders(email: Optional[str] = None, db: Session = Depends(get_db)):
    if email:
        orders = crud.get_orders_by_email(db, email=email)
    else:
        orders = crud.get_all_orders(db)
    if not orders:
        raise HTTPException(status_code=404, detail="Item not found")
    return orders


# GET order from orders by ID
@app.get("/orders/{order_id}", tags=['orders'])
def read_order_by_order_id(order_id: int, db: Session = Depends(get_db)):
    order_id = crud.get_order_by_id(db, order_id=order_id)
    if order_id is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return order_id


# POST an order to orders
@app.post("/orders", status_code=201, tags=['orders'])
def post_order_to_orders(order: schemas.AddOrder, db: Session = Depends(get_db)):
    return crud.add_order(db=db, order=order)


# PATCH data in an order from orders
@app.patch("/orders/{order_id}", tags=['orders'])
def patch_data_in_order(order_id: int, order: schemas.EditOrder, db: Session = Depends(get_db)):
    return crud.edit_order_in_orders(db=db, order_id=order_id, order=order)


# DELETE order from orders
@app.delete("/orders/{order_id}", status_code=204, response_class=Response, tags=['orders'])
def del_order_from_orders(order_id: int, db: Session = Depends(get_db)):
    crud.del_order_from_orders(db=db, order_id=order_id)


# ORDEREDITEMS


# GET All ordered items from ordereditems
@app.get("/ordereditems", tags=['ordereditems'])
def read_ordereditems(db: Session = Depends(get_db)):
    ordereditems = crud.get_all_ordereditems(db)
    if not ordereditems:
        raise HTTPException(status_code=404, detail="Item not found")
    return ordereditems


# GET ordered item from ordereditems by OrderedItemID
@app.get("/ordereditems/{ordered_item_id}", tags=['ordereditems'])
def read_ordereditem_by_ordered_item_id(ordered_item_id: int, db: Session = Depends(get_db)):
    ordereditem = crud.get_ordereditem_by_ordered_item_id(db, ordered_item_id=ordered_item_id)
    if ordereditem is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return ordereditem


# GET ordered items from ordereditems by OrderID
@app.get("/ordereditems/orderid/{order_id}", tags=['ordereditems'])
def read_ordereditems_by_order_id(order_id: int, db: Session = Depends(get_db)):
    ordereditems = crud.get_ordereditems_by_order_id(db, order_id=order_id)
    if ordereditems is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return ordereditems


# GET ordered items from ordereditems by MenuID
@app.get("/ordereditems/menuid/{menu_id}", tags=['ordereditems'])
def read_ordereditems_by_menu_id(menu_id: int, db: Session = Depends(get_db)):
    ordereditems = crud.get_ordereditems_by_menu_id(db, menu_id=menu_id)
    if ordereditems is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return ordereditems


# POST an ordered item to ordereditems
@app.post("/ordereditems", status_code=201, tags=['ordereditems'])
def post_ordereditem_to_ordereditems(ordereditem: schemas.AddOrderedItem, db: Session = Depends(get_db)):
    return crud.add_ordereditem_to_ordereditems(db=db, ordereditem=ordereditem)


# PATCH data in an ordered item from ordereditems
@app.patch("/ordereditems/{ordered_item_id}", tags=['ordereditems'])
def patch_data_in_ordereditem(ordered_item_id: int, ordereditem: schemas.EditOrderedItem,
                              db: Session = Depends(get_db)):
    return crud.edit_data_in_ordereditem(db=db, ordered_item_id=ordered_item_id, ordereditem=ordereditem)


# DELETE ordered item from ordereditems
@app.delete("/ordereditems/{ordered_item_id}", status_code=204, response_class=Response, tags=['ordereditems'])
def del_ordereditem_from_ordereditems(ordered_item_id: int, db: Session = Depends(get_db)):
    crud.del_ordereditem_from_ordereditems(db=db, ordered_item_id=ordered_item_id)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
