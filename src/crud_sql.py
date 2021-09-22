import re

import psycopg2
from fastapi import HTTPException

from src import config
from src import schemas

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


def query_to_database_processor(query):
    conn = None
    cur = None
    try:
        params = config.config()
        params.popitem()  # USE_ORM parameter is not used in psycopg2
        params.popitem()  # database_url parameter is not used in psycopg2
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(query)
        data = cur.fetchall()
        column_names = [value[0] for value in cur.description]
        results = [dict(zip(column_names, row)) for row in data]
        if not results:
            return None
        return results
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            if cur is not None:
                cur.close()
            cur.close()
            conn.close()


def schema_processor_for_inserting(schema):
    # schema example structure: [("name", "Pepperoni"), ("price", "23.0")]
    headers, values = [], []
    for header, value in schema:
        if value is None or header == "ordered_items":
            continue
        headers.append(header)
        values.append(value)
    headers_string = '"' + '", "'.join(map(str, headers)) + '"'  # headers needs to be in format: "name", "price"
    values_string = "'" + "', '".join(map(str, values)) + "'"  # values needs to be in format: 'Pepperoni', '23.0'
    return headers_string, values_string


def schema_processor_for_patching(schema):
    update_string = ""
    for header, value in schema:
        if value is None:
            continue
        update_string = update_string + f""""{str(header)}" = '{str(value)}', """
    update_string = update_string[:-2]  # update_string needs to be in format: "name" = 'Veggi', "price" = '21.0'
    return update_string


# MENU


def get_all_menu_items(db):
    query = "SELECT * FROM menu_items"
    return query_to_database_processor(query)


def get_menu_items_by_name(name: str, db):
    query = f"""SELECT * FROM menu_items WHERE "name" ILIKE '%{name}%'"""
    return query_to_database_processor(query)


def get_menu_items_by_category(category: str, db):
    query = f"""SELECT * FROM menu_items WHERE "category" ILIKE '%{category}%'"""
    return query_to_database_processor(query)


def get_menu_item_by_id(id: int, db):
    query = f"""SELECT * FROM menu_items WHERE "id" = {id}"""
    results = query_to_database_processor(query)
    if results is None:
        return results
    else:
        return results[0]


def add_to_menu_items(item: schemas.AddItem, db):
    headers, values = schema_processor_for_inserting(item)
    query = f"""INSERT INTO menu_items ({headers}) VALUES ({values}) RETURNING * """
    return query_to_database_processor(query)[0]


def edit_item_in_menu_items(id: int, item: schemas.EditItem, db):
    query = f"""SELECT * FROM menu_items WHERE "id" = {id} """
    results = query_to_database_processor(query)
    if not results:
        raise HTTPException(status_code=404, detail="Item not found")
    update_string = schema_processor_for_patching(item)
    if update_string != "":
        query = f"""UPDATE menu_items SET {update_string} WHERE "id" = {id} RETURNING * """
        results = query_to_database_processor(query)
    return results[0]


def del_item_from_menu_items(id: int, db):
    query = f"""SELECT * FROM menu_items WHERE "id" = {id} """
    results = query_to_database_processor(query)
    if not results:
        raise HTTPException(status_code=404, detail="Item not found")
    query = f"""SELECT "order_id" FROM ordered_items WHERE "menu_item_id" = {id} """
    results = query_to_database_processor(query)
    query = f"""DELETE FROM menu_items WHERE "id" = {id}"""
    query_to_database_processor(query)

    if results is not None:
        for row in results:
            recalculate_total_price_value(row['order_id'], db)


# ORDERS


def get_all_orders(db):
    query = "SELECT * FROM orders"
    return query_to_database_processor(query)


def get_orders_by_email(email: str, db):
    query = f"""SELECT * FROM orders WHERE "email" ILIKE '%{email}%'"""
    return query_to_database_processor(query)


def get_order_by_id(id: int, db):
    query = f"""SELECT * FROM orders WHERE "id" = {id}"""
    results = query_to_database_processor(query)
    if results is None:
        return results
    else:
        return results[0]


def add_to_orders(order: schemas.AddOrder, db):
    if order.email is not None:
        if not EMAIL_REGEX.match(order.email):
            raise HTTPException(status_code=400, detail="email is invalid")
    headers, values = schema_processor_for_inserting(order)
    if headers != '""':  # check if starting order is empty
        query = f"""INSERT INTO orders ({headers}, "total_price") VALUES ({values}, '0') RETURNING * """
    else:
        query = f"""INSERT INTO orders ("total_price") VALUES ('0') RETURNING * """
    results = query_to_database_processor(query)
    if order.ordered_items is not None:
        order_id = results[0]['id']
        for ordered_item in order.ordered_items:
            query = f"""SELECT * FROM menu_items WHERE "id" = {ordered_item.menu_item_id} """
            results = query_to_database_processor(query)
            if not results:
                raise HTTPException(status_code=404, detail="Item not found")

            query = f"""SELECT "price" FROM menu_items WHERE "id" = {ordered_item.menu_item_id}"""
            results_for_ordereditem = query_to_database_processor(query)
            price = results_for_ordereditem[0]['price']

            headers, values = schema_processor_for_inserting(ordered_item)
            query = f"""INSERT INTO ordered_items ("order_id", {headers}, "unit_price") VALUES ('{order_id}', {values}, '{price}')"""
            query_to_database_processor(query)
        recalculate_total_price_value(order_id, db)
        query = f"""SELECT * FROM orders WHERE "id" = {order_id}"""
        results = query_to_database_processor(query)
    return results[0]


def edit_item_in_orders(id: int, order: schemas.EditOrder, db):
    query = f"""SELECT * FROM orders WHERE "id" = {id} """
    results = query_to_database_processor(query)
    if not results:
        raise HTTPException(status_code=404, detail="Item not found")
    if order.email is not None:
        if not EMAIL_REGEX.match(order.email):
            raise HTTPException(status_code=400, detail="email is invalid")
    update_string = schema_processor_for_patching(order)
    if update_string != "":
        query = f"""UPDATE orders SET {update_string} WHERE "id" = {id} RETURNING * """
        results = query_to_database_processor(query)
    return results[0]


def del_item_from_orders(id: int, db):
    query = f"""SELECT * FROM orders WHERE "id" = {id} """
    results = query_to_database_processor(query)
    if not results:
        raise HTTPException(status_code=404, detail="Item not found")
    query = f"""DELETE FROM orders WHERE "id" = {id} """
    query_to_database_processor(query)


# ORDEREDITEMS


def get_all_ordered_items(db):
    query = "SELECT * FROM ordered_items"
    return query_to_database_processor(query)


def get_ordered_item_by_id(id: int, db):
    query = f"""SELECT * FROM ordered_items WHERE "id" = {id}"""
    results = query_to_database_processor(query)
    if results is None:
        return results
    else:
        return results[0]


def get_ordered_items_by_order_id(order_id: int, db):
    query = f"""SELECT * FROM ordered_items WHERE "order_id" = {order_id}"""
    return query_to_database_processor(query)


def get_ordered_items_by_menu_item_id(menu_item_id: int, db):
    query = f"""SELECT * FROM ordered_items WHERE "menu_item_id" = {menu_item_id}"""
    return query_to_database_processor(query)


def add_to_ordered_items(ordered_item: schemas.AddOrderedItem, db):
    query = f"""SELECT * FROM menu_items WHERE "id" = {ordered_item.menu_item_id} """
    results = query_to_database_processor(query)
    if not results:
        raise HTTPException(status_code=404, detail="Item not found")
    query = f"""SELECT * FROM orders WHERE "id" = {ordered_item.order_id} """
    results = query_to_database_processor(query)
    if not results:
        raise HTTPException(status_code=404, detail="Item not found")

    query = f"""SELECT "price" FROM menu_items WHERE "id" = {ordered_item.menu_item_id}"""
    results = query_to_database_processor(query)
    price = results[0]['price']

    headers, values = schema_processor_for_inserting(ordered_item)
    query = f"""INSERT INTO ordered_items ({headers}, "unit_price") VALUES ({values}, '{price}') RETURNING * """
    results = query_to_database_processor(query)
    recalculate_total_price_value(results[0]['order_id'], db)
    return results[0]


def edit_item_in_ordered_items(id: int, ordered_item: schemas.EditOrderedItem, db):
    query = f"""SELECT * FROM ordered_items WHERE "id" = {id} """
    results = query_to_database_processor(query)
    if not results:
        raise HTTPException(status_code=404, detail="Item not found")
    if ordered_item.menu_item_id is not None:
        query = f"""SELECT * FROM menu_items WHERE "id" = {ordered_item.menu_item_id} """
        results_to_check = query_to_database_processor(query)
        if not results_to_check:
            raise HTTPException(status_code=404, detail="Item not found")
    if ordered_item.order_id is not None:
        query = f"""SELECT * FROM orders WHERE "id" = {ordered_item.order_id} """
        results_to_check = query_to_database_processor(query)
        if not results_to_check:
            raise HTTPException(status_code=404, detail="Item not found")

    update_string = schema_processor_for_patching(ordered_item)
    if update_string != "":
        query = f"""UPDATE ordered_items SET {update_string} WHERE "id" = {id} RETURNING * """
        results = query_to_database_processor(query)

        # If price was not set manually, prepare unit_price value from Menu
        if ordered_item.unit_price is None:
            query = f"""SELECT "price" FROM menu_items WHERE "id" = {ordered_item.menu_item_id}"""
            results_for_ordereditem = query_to_database_processor(query)
            price = results_for_ordereditem[0]['price']

            query = f"""UPDATE ordered_items SET "unit_price" = '{price}' WHERE "id" = {id} RETURNING *"""
            results = query_to_database_processor(query)
    recalculate_total_price_value(results[0]['order_id'], db)
    return results[0]


def del_item_from_ordered_items(id: int, db):
    query = f"""SELECT * FROM ordered_items WHERE "id" = {id} """
    results = query_to_database_processor(query)
    if not results:
        raise HTTPException(status_code=404, detail="Item not found")
    query = f"""DELETE FROM ordered_items WHERE "id" = {id} """
    query_to_database_processor(query)

    recalculate_total_price_value(results[0]['order_id'], db)


# "TRIGGERS"

def recalculate_total_price_value(order_id, db):
    query = f"""SELECT * FROM ordered_items WHERE "order_id" = {order_id} """
    results = query_to_database_processor(query)
    total_price = 0
    if not results:
        query = f"""UPDATE orders SET "total_price" = {total_price} WHERE "id" = {order_id} RETURNING * """
    else:
        for item in results:
            total_price += int(item['quantity']) * float(item['unit_price'])
        query = f"""UPDATE orders SET "total_price" = {total_price} WHERE "id" = {order_id} RETURNING * """
    query_to_database_processor(query)
