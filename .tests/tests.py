"""
    Run: pytest .tests\tests.py
"""

import json

import requests

url = "http://127.0.0.1:8000"

# REST API CRUD FUNCTIONALITY  TESTS

# MENU TESTS

menu_id = 0  # needed to pass information between tests


def test_menu_endpoint_status_code_equals_200():
    response = requests.get(url + "/menu")
    assert response.status_code == 200


def test_menu_item_get_endpoint():
    response = requests.get(url + "/menu/1")
    resp_body = response.json()
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert type(resp_body['name']) == str
    assert type(resp_body['menu_id']) == int
    assert type(resp_body['price']) == float
    assert type(resp_body['category']) == str


def test_menu_item_post_endpoint():
    global menu_id
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "name": "Pepperoni",
        "price": 23,
        "category": "Pizza"
    }
    response = requests.post(url + "/menu", data=json.dumps(data),
                             headers=headers)
    resp_body = response.json()
    menu_id = resp_body['menu_id']
    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json"
    assert type(resp_body['name']) == str
    assert type(resp_body['menu_id']) == int
    assert type(resp_body['price']) == float
    assert type(resp_body['category']) == str


def test_menu_item_patch_endpoint():
    global menu_id
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "name": "Changed",
        "price": 50,
        "category": "New category"
    }
    response = requests.patch(url + "/menu/" + str(menu_id), data=json.dumps(data),
                              headers=headers)
    resp_body = response.json()
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert type(resp_body['name']) == str
    assert type(resp_body['menu_id']) == int
    assert type(resp_body['price']) == float
    assert type(resp_body['category']) == str


def test_menu_item_delete_endpoint():
    global menu_id
    response = requests.delete(url + "/menu/" + str(menu_id))
    assert response.status_code == 204


def test_menu_wrong_id_get_endpoint():
    response = requests.get(url + "/menu/0")
    resp_body = response.json()
    assert response.status_code == 404
    assert type(resp_body['detail']) == str


# ORDERS AND ORDEREDITEMS TEST

order_id = 0  # needed to pass information between tests
ordered_item_id = 0  # needed to pass information between tests


# ORDERS TESTS


def test_orders_post_endpoint():
    global order_id
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "comments": "Test comment",
        "email": "test@email.com",
        "ordered_items": [
            {
                "menu_id": 1,
                "quantity": 1
            },
            {
                "menu_id": 18,
                "quantity": 2
            }
        ]
    }
    response = requests.post(url + "/orders", data=json.dumps(data),
                             headers=headers)
    resp_body = response.json()
    order_id = resp_body['order_id']
    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json"
    assert type(resp_body['comments']) == str
    assert type(resp_body['order_id']) == int
    assert type(resp_body['email']) == str
    assert type(resp_body['total_price']) == float


def test_orders_endpoint_status_code_equals_200():
    response = requests.get(url + "/orders")
    assert response.status_code == 200


def test_orders_get_by_id_endpoint():
    response = requests.get(url + "/orders/" + str(order_id))
    resp_body = response.json()
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert type(resp_body['comments']) == str
    assert type(resp_body['order_id']) == int
    assert type(resp_body['email']) == str
    assert type(resp_body['total_price']) == float


def test_orders_patch_data_endpoint():
    global order_id
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "comments": "Test comment changed",
        "email": "test@changed.com"
    }
    response = requests.patch(url + "/orders/" + str(order_id), data=json.dumps(data),
                              headers=headers)
    resp_body = response.json()
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert type(resp_body['comments']) == str
    assert type(resp_body['order_id']) == int
    assert type(resp_body['email']) == str
    assert type(resp_body['total_price']) == float


# ORDEREDITEMS TESTS


def test_ordereditems_post_endpoint():
    global order_id
    global ordered_item_id
    global menu_id
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    menu_id = 17
    data = {
        "menu_id": menu_id,
        "order_id": order_id,
        "quantity": 3
    }
    response = requests.post(url + "/ordereditems", data=json.dumps(data),
                             headers=headers)
    resp_body = response.json()
    ordered_item_id = resp_body['ordered_item_id']
    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json"
    assert type(resp_body['quantity']) == int
    assert type(resp_body['menu_id']) == int
    assert type(resp_body['ordered_item_id']) == int
    assert type(resp_body['unit_price']) == float
    assert type(resp_body['order_id']) == int


def test_ordereditems_endpoint_status_code_equals_200():
    response = requests.get(url + "/ordereditems")
    assert response.status_code == 200


def test_ordereditems_get_by_id_endpoint():
    response = requests.get(url + "/ordereditems/" + str(ordered_item_id))
    resp_body = response.json()
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert type(resp_body['quantity']) == int
    assert type(resp_body['menu_id']) == int
    assert type(resp_body['ordered_item_id']) == int
    assert type(resp_body['unit_price']) == float
    assert type(resp_body['order_id']) == int


def test_ordereditems_orderid_get_by_id_endpoint():
    response = requests.get(url + "/ordereditems/order_id/" + str(order_id))
    assert response.status_code == 200


def test_ordereditems_menuid_get_by_id_endpoint():
    response = requests.get(url + "/ordereditems/menu_id/" + str(menu_id))
    assert response.status_code == 200


def test_ordereditems_ordereditem_patch_endpoint():
    global menu_id
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "menu_id": 18,
        "order_id": order_id,
        "quantity": 4,
        "unit_price": 7
    }
    response = requests.patch(url + "/ordereditems/" + str(ordered_item_id), data=json.dumps(data),
                              headers=headers)
    resp_body = response.json()
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert type(resp_body['quantity']) == int
    assert type(resp_body['menu_id']) == int
    assert type(resp_body['ordered_item_id']) == int
    assert type(resp_body['unit_price']) == float
    assert type(resp_body['order_id']) == int


def test_ordereditems_ordereditem_delete_endpoint():
    global menu_id
    response = requests.delete(url + "/ordereditems/" + str(ordered_item_id))
    assert response.status_code == 204


def test_ordereditems_wrong_id_get_endpoint():
    response = requests.get(url + "/ordereditems/0")
    resp_body = response.json()
    assert response.status_code == 404
    assert type(resp_body['detail']) == str


# LAST TEST FOR ORDERS

def test_orders_order_delete_endpoint():
    global order_id
    response = requests.delete(url + "/orders/" + str(order_id))
    assert response.status_code == 204


def test_orders_wrong_id_get_endpoint():
    response = requests.get(url + "/orders/0")
    resp_body = response.json()
    assert response.status_code == 404
    assert type(resp_body['detail']) == str


# DIFFERENT SCENARIO TESTS


# GENERAL TEST TO CALCULATE IF TOTAL price IS CORRECT

def test_order_to_check_total_price():
    global order_id
    global ordered_item_id

    # Create an Order
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {}
    response = requests.post(url + "/orders", data=json.dumps(data),
                             headers=headers)
    resp_body = response.json()
    order_id = resp_body['order_id']
    assert resp_body['total_price'] == 0

    # Add item to Order
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "menu_id": 17,
        "order_id": order_id,
        "quantity": 3
    }
    response = requests.post(url + "/ordereditems", data=json.dumps(data),
                             headers=headers)
    resp_body = response.json()
    ordered_item_id = resp_body['ordered_item_id']

    # Assert if total_price is correct
    total_price_should_be = resp_body['unit_price'] * resp_body['quantity']

    response = requests.get(url + "/orders/" + str(order_id))
    resp_body = response.json()
    assert resp_body['total_price'] == total_price_should_be

    # Edit item unit_price attribute
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "unit_price": 10
    }
    response = requests.patch(url + "/ordereditems/" + str(ordered_item_id), data=json.dumps(data),
                              headers=headers)
    resp_body = response.json()

    # Assert if total_price is correct
    total_price_should_be = resp_body['unit_price'] * resp_body['quantity']

    response = requests.get(url + "/orders/" + str(order_id))
    resp_body = response.json()
    assert resp_body['total_price'] == total_price_should_be

    # Delete item
    requests.delete(url + "/ordereditems/" + str(ordered_item_id))

    # Assert if total_price is now equal 0
    response = requests.get(url + "/orders/" + str(order_id))
    resp_body = response.json()
    assert resp_body['total_price'] == 0

    # Finally delete order
    requests.delete(url + "/orders/" + str(order_id))


def test_post_not_enough_data_in_menu():
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "name": "Not enough data"
    }
    response = requests.post(url + "/menu", data=json.dumps(data),
                             headers=headers)
    resp_body = response.json()
    assert response.status_code == 422
    assert resp_body['detail'][0]['msg'] == "field required"
    assert resp_body['detail'][0]['type'] == "value_error.missing"


def test_post_lorem_ipsum_to_orders():
    global order_id
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " \
           "Phasellus at elit risus. Nulla et consectetur felis. Cras quis ultricies lacus. " \
           "Fusce vulputate est risus, nec gravida enim sagittis vel. " \
           "Duis ligula magna, finibus nec est sed, cursus sodales purus. In ut diam eget dui sollicitudin semper. " \
           "Morbi sodales mi sed est tempor condimentum. Vivamus a porttitor ipsum. Ut ut iaculis augue. " \
           "Quisque lacinia est ornare justo mollis feugiat. Sed hendrerit porta metus et tempor."

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "comments": text
    }
    response = requests.post(url + "/orders", data=json.dumps(data),
                             headers=headers)
    assert response.status_code == 201
    resp_body = response.json()
    order_id = resp_body['order_id']
    requests.delete(url + "/orders/" + str(order_id))


def test_post_none_to_menu():
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "name": None,
        "price": None,
        "category": None
    }
    response = requests.post(url + "/menu", data=json.dumps(data),
                             headers=headers)
    resp_body = response.json()
    assert response.status_code == 422
    assert resp_body['detail'][0]['msg'] == "none is not an allowed value"
    assert resp_body['detail'][0]['type'] == "type_error.none.not_allowed"
