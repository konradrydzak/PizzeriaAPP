"""
    Run: pytest .tests\tests.py
"""

import json

import requests

url = "http://127.0.0.1:8000"

''' REST API CRUD FUNCTIONALITY  TESTS '''

''' MENU TESTS '''

MenuID = 0  # global variable


def test_menu_endpoint_status_code_equals_200():
    response = requests.get(url + "/menu")
    assert response.status_code == 200


def test_menu_item_get_endpoint():
    response = requests.get(url + "/menu/1")
    resp_body = response.json()
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert type(resp_body['Name']) == str
    assert type(resp_body['MenuID']) == int
    assert type(resp_body['Price']) == float
    assert type(resp_body['Category']) == str


def test_menu_item_post_endpoint():
    global MenuID
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "Name": "Pepperoni",
        "Price": 23,
        "Category": "Pizza"
    }
    response = requests.post(url + "/menu", data=json.dumps(data),
                             headers=headers)
    resp_body = response.json()
    MenuID = resp_body['MenuID']
    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json"
    assert type(resp_body['Name']) == str
    assert type(resp_body['MenuID']) == int
    assert type(resp_body['Price']) == float
    assert type(resp_body['Category']) == str


def test_menu_item_patch_endpoint():
    global MenuID
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "Name": "Changed",
        "Price": 50,
        "Category": "New category"
    }
    response = requests.patch(url + "/menu/" + str(MenuID), data=json.dumps(data),
                              headers=headers)
    resp_body = response.json()
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert type(resp_body['Name']) == str
    assert type(resp_body['MenuID']) == int
    assert type(resp_body['Price']) == float
    assert type(resp_body['Category']) == str


def test_menu_item_delete_endpoint():
    global MenuID
    response = requests.delete(url + "/menu/" + str(MenuID))
    assert response.status_code == 204


def test_menu_wrong_id_get_endpoint():
    response = requests.get(url + "/menu/0")
    resp_body = response.json()
    assert response.status_code == 404
    assert type(resp_body['detail']) == str


''' ORDERS AND ORDEREDITEMS TEST '''

OrderID = 0  # global variable
OrderedItemID = 0  # global variable

''' ORDERS TESTS '''


def test_orders_post_endpoint():
    global OrderID
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "Comments": "Test comment",
        "Email": "test@email.com",
        "OrderedItems": [
            {
                "MenuID": 1,
                "Quantity": 1
            },
            {
                "MenuID": 18,
                "Quantity": 2
            }
        ]
    }
    response = requests.post(url + "/orders", data=json.dumps(data),
                             headers=headers)
    resp_body = response.json()
    OrderID = resp_body['OrderID']
    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json"
    assert type(resp_body['Comments']) == str
    assert type(resp_body['OrderID']) == int
    assert type(resp_body['Email']) == str
    assert type(resp_body['TotalPrice']) == float


def test_orders_endpoint_status_code_equals_200():
    response = requests.get(url + "/orders")
    assert response.status_code == 200


def test_orders_get_by_id_endpoint():
    response = requests.get(url + "/orders/" + str(OrderID))
    resp_body = response.json()
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert type(resp_body['Comments']) == str
    assert type(resp_body['OrderID']) == int
    assert type(resp_body['Email']) == str
    assert type(resp_body['TotalPrice']) == float


def test_orders_patch_data_endpoint():
    global OrderID
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "Comments": "Test comment changed",
        "Email": "test@changed.com"
    }
    response = requests.patch(url + "/orders/" + str(OrderID), data=json.dumps(data),
                              headers=headers)
    resp_body = response.json()
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert type(resp_body['Comments']) == str
    assert type(resp_body['OrderID']) == int
    assert type(resp_body['Email']) == str
    assert type(resp_body['TotalPrice']) == float


''' ORDEREDITEMS TESTS '''


def test_ordereditems_post_endpoint():
    global OrderID
    global OrderedItemID
    global MenuID
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    MenuID = 17
    data = {
        "MenuID": MenuID,
        "OrderID": OrderID,
        "Quantity": 3
    }
    response = requests.post(url + "/ordereditems", data=json.dumps(data),
                             headers=headers)
    resp_body = response.json()
    OrderedItemID = resp_body['OrderedItemID']
    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json"
    assert type(resp_body['Quantity']) == int
    assert type(resp_body['MenuID']) == int
    assert type(resp_body['OrderedItemID']) == int
    assert type(resp_body['UnitPrice']) == float
    assert type(resp_body['OrderID']) == int


def test_ordereditems_endpoint_status_code_equals_200():
    response = requests.get(url + "/ordereditems")
    assert response.status_code == 200


def test_ordereditems_get_by_id_endpoint():
    response = requests.get(url + "/ordereditems/" + str(OrderedItemID))
    resp_body = response.json()
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert type(resp_body['Quantity']) == int
    assert type(resp_body['MenuID']) == int
    assert type(resp_body['OrderedItemID']) == int
    assert type(resp_body['UnitPrice']) == float
    assert type(resp_body['OrderID']) == int


def test_ordereditems_orderid_get_by_id_endpoint():
    response = requests.get(url + "/ordereditems/orderid/" + str(OrderID))
    assert response.status_code == 200


def test_ordereditems_menuid_get_by_id_endpoint():
    response = requests.get(url + "/ordereditems/menuid/" + str(MenuID))
    assert response.status_code == 200


def test_ordereditems_ordereditem_patch_endpoint():
    global MenuID
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "MenuID": 18,
        "OrderID": OrderID,
        "Quantity": 4,
        "UnitPrice": 7
    }
    response = requests.patch(url + "/ordereditems/" + str(OrderedItemID), data=json.dumps(data),
                              headers=headers)
    resp_body = response.json()
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert type(resp_body['Quantity']) == int
    assert type(resp_body['MenuID']) == int
    assert type(resp_body['OrderedItemID']) == int
    assert type(resp_body['UnitPrice']) == float
    assert type(resp_body['OrderID']) == int


def test_ordereditems_ordereditem_delete_endpoint():
    global MenuID
    response = requests.delete(url + "/ordereditems/" + str(OrderedItemID))
    assert response.status_code == 204


def test_ordereditems_wrong_id_get_endpoint():
    response = requests.get(url + "/ordereditems/0")
    resp_body = response.json()
    assert response.status_code == 404
    assert type(resp_body['detail']) == str


# LAST TEST FOR ORDERS

def test_orders_order_delete_endpoint():
    global OrderID
    response = requests.delete(url + "/orders/" + str(OrderID))
    assert response.status_code == 204


def test_orders_wrong_id_get_endpoint():
    response = requests.get(url + "/orders/0")
    resp_body = response.json()
    assert response.status_code == 404
    assert type(resp_body['detail']) == str


# GENERAL TEST TO CALCULATE IF TOTAL PRICE IS GOOD
def test_order_to_check_total_price():
    global OrderID
    global OrderedItemID

    # Create an Order
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {}
    response = requests.post(url + "/orders", data=json.dumps(data),
                             headers=headers)
    resp_body = response.json()
    OrderID = resp_body['OrderID']
    assert resp_body['TotalPrice'] == 0

    # Add item to Order
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "MenuID": 17,
        "OrderID": OrderID,
        "Quantity": 3
    }
    response = requests.post(url + "/ordereditems", data=json.dumps(data),
                             headers=headers)
    resp_body = response.json()
    OrderedItemID = resp_body['OrderedItemID']

    # Assert if TotalPrice is correct
    TotalPriceShouldBe = resp_body['UnitPrice'] * resp_body['Quantity']

    response = requests.get(url + "/orders/" + str(OrderID))
    resp_body = response.json()
    assert resp_body['TotalPrice'] == TotalPriceShouldBe

    # Edit item UnitPrice attribute
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "UnitPrice": 10
    }
    response = requests.patch(url + "/ordereditems/" + str(OrderedItemID), data=json.dumps(data),
                              headers=headers)
    resp_body = response.json()

    # Assert if TotalPrice is correct
    TotalPriceShouldBe = resp_body['UnitPrice'] * resp_body['Quantity']

    response = requests.get(url + "/orders/" + str(OrderID))
    resp_body = response.json()
    assert resp_body['TotalPrice'] == TotalPriceShouldBe

    # Delete item
    requests.delete(url + "/ordereditems/" + str(OrderedItemID))

    # Assert if TotalPrice is now equal 0
    response = requests.get(url + "/orders/" + str(OrderID))
    resp_body = response.json()
    assert resp_body['TotalPrice'] == 0

    # Finally delete order
    requests.delete(url + "/orders/" + str(OrderID))


''' DIFFERENT SCENARIO TESTS '''


def test_post_not_enough_data_in_menu():
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "Name": "Not enough data"
    }
    response = requests.post(url + "/menu", data=json.dumps(data),
                             headers=headers)
    resp_body = response.json()
    assert response.status_code == 422
    assert resp_body['detail'][0]['msg'] == "field required"
    assert resp_body['detail'][0]['type'] == "value_error.missing"


def test_post_lorem_ipsum_to_orders():
    global OrderID
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
        "Comments": text
    }
    response = requests.post(url + "/orders", data=json.dumps(data),
                             headers=headers)
    assert response.status_code == 201
    resp_body = response.json()
    OrderID = resp_body['OrderID']
    requests.delete(url + "/orders/" + str(OrderID))


def test_post_none_to_menu():
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = {
        "Name": None,
        "Price": None,
        "Category": None
    }
    response = requests.post(url + "/menu", data=json.dumps(data),
                             headers=headers)
    resp_body = response.json()
    assert response.status_code == 422
    assert resp_body['detail'][0]['msg'] == "none is not an allowed value"
    assert resp_body['detail'][0]['type'] == "type_error.none.not_allowed"
