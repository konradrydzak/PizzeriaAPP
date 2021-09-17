import re

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src import schemas

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


def schema_processor_for_inserting(schema):
    # schema example structure: [("Name", "Pepperoni"), ("Price", "23.0")]
    headers, values = [], []
    for value in schema:
        if value[1] is None or value[0] == "OrderedItems":
            continue
        headers.append(value[0])
        values.append(value[1])
    headers_string = '"' + '", "'.join(map(str, headers)) + '"'  # headers needs to be in format: "Name", "Price"
    values_string = "'" + "', '".join(map(str, values)) + "'"  # values needs to be in format: 'Pepperoni', '23.0'
    return headers_string, values_string


def schema_processor_for_patching(schema):
    update_string = ""
    for value in schema:
        if value[1] is None:
            continue
        update_string = update_string + f""""{str(value[0])}" = '{str(value[1])}', """
    update_string = update_string[:-2]  # update_string needs to be in format: "Name" = 'Veggi', "Price" = '21.0'
    return update_string


# MENU


def get_all_menu(db: Session):
    query = "SELECT * FROM menu"
    data = db.execute(query)
    results = [{**i} for i in data]
    if not results:
        return None
    return results


def get_menu_items_by_name(db: Session, name: str):
    query = f"""SELECT * FROM menu WHERE "Name" ILIKE '%{name}%'"""
    data = db.execute(query)
    results = [{**i} for i in data]
    if not results:
        return None
    return results


def get_menu_items_by_category(db: Session, category: str):
    query = f"""SELECT * FROM menu WHERE "Category" ILIKE '%{category}%'"""
    data = db.execute(query)
    results = [{**i} for i in data]
    if not results:
        return None
    return results


def get_menu_item_by_id(db: Session, menu_id: int):
    query = f"""SELECT * FROM menu WHERE "MenuID" = {menu_id}"""
    data = db.execute(query)
    results = [{**i} for i in data]
    if not results:
        return None
    return results[0]


def add_item_to_menu(db: Session, item: schemas.AddItem):
    headers, values = schema_processor_for_inserting(item)
    query = f"""INSERT INTO menu ({headers}) VALUES ({values}) RETURNING * """
    data = db.execute(query)
    db.commit()
    results = [{**i} for i in data]
    if not results:
        return None
    return results[0]


def edit_item_in_menu(db: Session, menu_id: int, item: schemas.EditItem):
    query = f"""SELECT * FROM menu WHERE "MenuID" = {menu_id} """
    data = db.execute(query)
    results = [{**i} for i in data]
    if not results:
        raise HTTPException(status_code=404, detail="Item not found")
    update_string = schema_processor_for_patching(item)
    query = f"""UPDATE menu SET {update_string} WHERE "MenuID" = {menu_id} RETURNING * """
    data = db.execute(query)
    db.commit()
    results = [{**i} for i in data]
    if not results:
        return None
    return results[0]


def del_item_from_menu(db: Session, menu_id: int):
    query = f"""SELECT * FROM menu WHERE "MenuID" = {menu_id} """
    data = db.execute(query)
    results = [{**i} for i in data]
    if not results:
        raise HTTPException(status_code=404, detail="Item not found")
    query = f"""SELECT "OrderID" FROM OrderedItems WHERE "MenuID" = {menu_id} """
    data = db.execute(query)
    results = [{**i} for i in data]
    query = f"""DELETE FROM menu WHERE "MenuID" = {menu_id}"""
    db.execute(query)
    db.commit()
    for row in results:
        recalculate_totalprice_value(db, row['OrderID'])


# ORDERS


def get_all_orders(db: Session):
    query = "SELECT * FROM orders"
    data = db.execute(query)
    results = [{**i} for i in data]
    if not results:
        return None
    return results


def get_orders_by_email(db: Session, email: str):
    query = f"""SELECT * FROM orders WHERE "Email" ILIKE '%{email}%'"""
    data = db.execute(query)
    results = [{**i} for i in data]
    if not results:
        return None
    return results


def get_order_by_id(db: Session, order_id: int):
    query = f"""SELECT * FROM orders WHERE "OrderID" = {order_id}"""
    data = db.execute(query)
    results = [{**i} for i in data]
    if not results:
        return None
    return results[0]


def add_order(db: Session, order: schemas.AddOrder):
    if order.Email is not None:
        if not EMAIL_REGEX.match(order.Email):
            raise HTTPException(status_code=400, detail="Email is invalid")
    headers, values = schema_processor_for_inserting(order)
    query = f"""INSERT INTO orders ({headers}, "TotalPrice") VALUES ({values}, '0') RETURNING * """
    data = db.execute(query)
    db.commit()
    results = [{**i} for i in data]
    if order.OrderedItems is not None:
        order_id = results[0]['OrderID']
        for ordereditem in order.OrderedItems:
            query = f"""SELECT * FROM menu WHERE "MenuID" = {ordereditem.MenuID} """
            data = db.execute(query)
            results = [{**i} for i in data]
            if not results:
                raise HTTPException(status_code=404, detail="Item not found")

            query = f"""SELECT "Price" FROM menu WHERE "MenuID" = {ordereditem.MenuID}"""
            data_for_ordereditem = db.execute(query)
            results_for_ordereditem = [{**i} for i in data_for_ordereditem]
            Price = results_for_ordereditem[0]['Price']

            headers, values = schema_processor_for_inserting(ordereditem)
            query = f"""INSERT INTO ordereditems ("OrderID", {headers}, "UnitPrice") VALUES ('{order_id}', {values}, '{Price}')"""
            db.execute(query)
            db.commit()
        recalculate_totalprice_value(db, order_id)
        query = f"""SELECT * FROM orders WHERE "OrderID" = {order_id}"""
        data = db.execute(query)
        results = [{**i} for i in data]
    if not results:
        return None
    return results[0]


def edit_order_in_orders(db: Session, order_id: int, order: schemas.EditOrder):
    query = f"""SELECT * FROM orders WHERE "OrderID" = {order_id} """
    data = db.execute(query)
    results = [{**i} for i in data]
    if not results:
        raise HTTPException(status_code=404, detail="Item not found")
    if order.Email is not None:
        if not EMAIL_REGEX.match(order.Email):
            raise HTTPException(status_code=400, detail="Email is invalid")
    update_string = schema_processor_for_patching(order)
    query = f"""UPDATE orders SET {update_string} WHERE "OrderID" = {order_id} RETURNING * """
    data = db.execute(query)
    db.commit()
    results = [{**i} for i in data]
    if not results:
        return None
    return results[0]


def del_order_from_orders(db: Session, order_id: int):
    query = f"""SELECT * FROM orders WHERE "OrderID" = {order_id} """
    data = db.execute(query)
    results = [{**i} for i in data]
    if not results:
        raise HTTPException(status_code=404, detail="Item not found")
    query = f"""DELETE FROM orders WHERE "OrderID" = {order_id} """
    db.execute(query)
    db.commit()


# ORDEREDITEMS


def get_all_ordereditems(db: Session):
    query = "SELECT * FROM ordereditems"
    data = db.execute(query)
    results = [{**i} for i in data]
    if not results:
        return None
    return results


def get_ordereditem_by_ordered_item_id(db: Session, ordered_item_id: int):
    query = f"""SELECT * FROM ordereditems WHERE "OrderedItemID" = {ordered_item_id}"""
    data = db.execute(query)
    results = [{**i} for i in data]
    if not results:
        return None
    return results[0]


def get_ordereditems_by_order_id(db: Session, order_id: int):
    query = f"""SELECT * FROM ordereditems WHERE "OrderID" = {order_id}"""
    data = db.execute(query)
    results = [{**i} for i in data]
    if not results:
        return None
    return results


def get_ordereditems_by_menu_id(db: Session, menu_id: int):
    query = f"""SELECT * FROM ordereditems WHERE "MenuID" = {menu_id}"""
    data = db.execute(query)
    results = [{**i} for i in data]
    if not results:
        return None
    return results


def add_ordereditem_to_ordereditems(db: Session, ordereditem: schemas.AddOrderedItem):
    query = f"""SELECT * FROM menu WHERE "MenuID" = {ordereditem.MenuID} """
    data = db.execute(query)
    results = [{**i} for i in data]
    if not results:
        raise HTTPException(status_code=404, detail="Item not found")
    query = f"""SELECT * FROM orders WHERE "OrderID" = {ordereditem.OrderID} """
    data = db.execute(query)
    results = [{**i} for i in data]
    if not results:
        raise HTTPException(status_code=404, detail="Item not found")

    query = f"""SELECT "Price" FROM menu WHERE "MenuID" = {ordereditem.MenuID}"""
    data = db.execute(query)
    results = [{**i} for i in data]
    Price = results[0]['Price']

    headers, values = schema_processor_for_inserting(ordereditem)
    query = f"""INSERT INTO ordereditems ({headers}, "UnitPrice") VALUES ({values}, '{Price}') RETURNING * """
    data = db.execute(query)
    db.commit()

    results = [{**i} for i in data]
    recalculate_totalprice_value(db, results[0]['OrderID'])
    if not results:
        return None
    return results[0]


def edit_data_in_ordereditem(db: Session, ordered_item_id: int, ordereditem: schemas.EditOrderedItem):
    query = f"""SELECT * FROM ordereditems WHERE "OrderedItemID" = {ordered_item_id} """
    data = db.execute(query)
    results = [{**i} for i in data]
    if not results:
        raise HTTPException(status_code=404, detail="Item not found")
    if ordereditem.MenuID is not None:
        query = f"""SELECT * FROM menu WHERE "MenuID" = {ordereditem.MenuID} """
        data = db.execute(query)
        results = [{**i} for i in data]
        if not results:
            raise HTTPException(status_code=404, detail="Item not found")
    if ordereditem.OrderID is not None:
        query = f"""SELECT * FROM orders WHERE "OrderID" = {ordereditem.OrderID} """
        data = db.execute(query)
        results = [{**i} for i in data]
        if not results:
            raise HTTPException(status_code=404, detail="Item not found")

    update_string = schema_processor_for_patching(ordereditem)
    query = f"""UPDATE ordereditems SET {update_string} WHERE "OrderedItemID" = {ordered_item_id} RETURNING * """
    data = db.execute(query)
    db.commit()

    # If price was not set manually, prepare UnitPrice value from Menu
    if ordereditem.UnitPrice is None:
        query = f"""SELECT "Price" FROM menu WHERE "MenuID" = {ordereditem.MenuID}"""
        data_for_ordereditem = db.execute(query)
        results_for_ordereditem = [{**i} for i in data_for_ordereditem]
        Price = results_for_ordereditem[0]['Price']

        query = f"""UPDATE ordereditems SET "UnitPrice" = '{Price}' WHERE "OrderedItemID" = {ordered_item_id} RETURNING *"""
        data = db.execute(query)
        db.commit()
    results = [{**i} for i in data]
    recalculate_totalprice_value(db, results[0]['OrderID'])
    if not results:
        return None
    return results[0]


def del_ordereditem_from_ordereditems(db: Session, ordered_item_id: int):
    query = f"""SELECT * FROM ordereditems WHERE "OrderedItemID" = {ordered_item_id} """
    data = db.execute(query)
    results = [{**i} for i in data]
    if not results:
        raise HTTPException(status_code=404, detail="Item not found")
    query = f"""DELETE FROM ordereditems WHERE "OrderedItemID" = {ordered_item_id} """
    db.execute(query)
    db.commit()
    recalculate_totalprice_value(db, results[0]['OrderID'])


# "TRIGGERS"

def recalculate_totalprice_value(db: Session, order_id):
    query = f"""SELECT * FROM ordereditems WHERE "OrderID" = {order_id} """
    data = db.execute(query)
    results = [{**i} for i in data]
    TotalPrice = 0
    if not results:
        query = f"""UPDATE orders SET "TotalPrice" = {TotalPrice} WHERE "OrderID" = {order_id} RETURNING * """
    else:
        for item in results:
            TotalPrice += int(item['Quantity']) * float(item['UnitPrice'])
        query = f"""UPDATE orders SET "TotalPrice" = {TotalPrice} WHERE "OrderID" = {order_id} RETURNING * """
    db.execute(query)
    db.commit()
