from typing import Optional

from pydantic import BaseModel, Field

''' MENU '''


class AddItem(BaseModel):
    Name: str
    Price: float = Field(None, gt=0, description="The price must be greater than zero")
    Category: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "Name": "Pepperoni",
                "Price": 23,
                "Category": "Pizza",
            }
        }


class EditItem(BaseModel):
    Name: Optional[str] = None
    Price: Optional[float] = Field(None, gt=0, description="The price must be greater than zero")
    Category: Optional[str] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "Name": "Pepperoni",
                "Price": 23,
                "Category": "Pizza",
            }
        }


''' ORDERS '''


class AddOrder(BaseModel):
    Comments: Optional[str] = None
    Email: Optional[str] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "Comments": "A comment for this order",
                "Email": "adress@email.com",
            }
        }


class EditOrder(BaseModel):
    TotalPrice: Optional[int] = Field(None, ge=0, description="The total price must be greater than or equal to zero")
    Comments: Optional[str] = None
    Email: Optional[str] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "TotalPrice": 42,
                "Comments": "A comment for this order",
                "Email": "adress@email.com",
            }
        }


''' ORDEREDITEMS '''


class AddOrderedItem(BaseModel):
    MenuID: int
    OrderID: int
    Quantity: int = Field(..., gt=0, description="The quantity must be greater than zero")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "MenuID": 17,
                "OrderID": 2,
                "Quantity": 3,
            }
        }


class EditOrderedItem(BaseModel):
    MenuID: Optional[int] = None
    OrderID: Optional[int] = None
    Quantity: int = Field(None, gt=0, description="The quantity must be greater than zero")
    UnitPrice: int = Field(None, gt=0, description="The unit price must be greater than zero")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "MenuID": 17,
                "OrderID": 2,
                "Quantity": 3,
                "UnitPrice": 7,
            }
        }
