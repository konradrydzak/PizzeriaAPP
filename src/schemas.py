from typing import Optional, List

from pydantic import BaseModel, Field

# MENU


class AddItem(BaseModel):
    name: str
    price: float = Field(None, gt=0, description="The price must be greater than zero")
    category: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Pepperoni",
                "price": 23,
                "category": "Pizza",
            }
        }


class EditItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = Field(None, gt=0, description="The price must be greater than zero")
    category: Optional[str] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Pepperoni",
                "price": 23,
                "category": "Pizza",
            }
        }


# ORDEREDITEMS


class BaseOrderedItem(BaseModel):
    menu_id: int
    quantity: int = Field(..., gt=0, description="The quantity must be greater than zero")

    class Config:
        orm_mode = True


class AddInitialOrderedItem(BaseOrderedItem):
    class Config:
        schema_extra = {
            "example": {
                "menu_id": 17,
                "quantity": 3,
            }
        }


class AddOrderedItem(BaseOrderedItem):
    order_id: int

    class Config:
        schema_extra = {
            "example": {
                "menu_id": 17,
                "order_id": 2,
                "quantity": 3,
            }
        }


class EditOrderedItem(BaseOrderedItem):
    menu_id: Optional[int] = None
    order_id: Optional[int] = None
    quantity: int = Field(None, gt=0, description="The quantity must be greater than zero")
    unit_price: int = Field(None, gt=0, description="The unit price must be greater than zero")

    class Config:
        schema_extra = {
            "example": {
                "menu_id": 17,
                "order_id": 2,
                "quantity": 3,
                "unit_price": 7,
            }
        }


# ORDERS


class BaseOrder(BaseModel):
    comments: Optional[str] = None
    email: Optional[str] = None

    class Config:
        orm_mode = True


class AddOrder(BaseOrder):
    ordered_items: Optional[List[AddInitialOrderedItem]] = None

    class Config:
        schema_extra = {
            "example": {
                "comments": "A comment for this order",
                "email": "adress@email.com",
                "ordered_items": [
                    {
                        "menu_id": 1,
                        "quantity": 1,
                    },
                    {
                        "menu_id": 18,
                        "quantity": 2,
                    },
                ]
            }
        }


class EditOrder(BaseOrder):
    total_price: Optional[int] = Field(None, ge=0, description="The total price must be greater than or equal to zero")

    class Config:
        schema_extra = {
            "example": {
                "total_price": 42,
                "comments": "A comment for this order",
                "email": "adress@email.com",
            }
        }
