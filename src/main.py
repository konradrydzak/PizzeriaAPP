from typing import Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.orm import Session

from src import models
from src import schemas, crud
from src.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET Full menu or some items from menu searched by name or by category
@app.get("/menu")
def read_menu(name: Optional[str] = None, category: Optional[str] = None, db: Session = Depends(get_db)):
    if name:
        menu = crud.get_menu_items_by_name(db, name=name)
    elif category:
        menu = crud.get_menu_items_by_category(db, category=category)
    else:
        menu = crud.get_menu_full(db)
    if not menu:
        raise HTTPException(status_code=404, detail="Item not found")
    return menu


# GET item from menu by ID
@app.get("/menu/{menu_id}")
def read_menu_item_by_id(menu_id: int, db: Session = Depends(get_db)):
    menu_item = crud.get_menu_item_by_id(db, menu_id=menu_id)
    if menu_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return menu_item


# POST an item to menu
@app.post("/menu/", status_code=201)
def post_item_to_menu(item: schemas.AddItem, db: Session = Depends(get_db)):
    return crud.add_item_to_menu(db=db, item=item)


# PATCH data into an item from menu
@app.patch("/menu/{menu_id}")
def put_data_in_item(menu_id: int, item: schemas.EditItem, db: Session = Depends(get_db)):
    return crud.edit_item_in_menu(db=db, menu_id=menu_id, item=item)


# DELETE item from menu
@app.delete("/menu/{menu_id}", status_code=204, response_class=Response)
def del_item_from_menu(menu_id: int, db: Session = Depends(get_db)):
    crud.del_item_from_menu(db=db, menu_id=menu_id)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
