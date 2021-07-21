from typing import Optional

from pydantic import BaseModel, Field

''' MENU '''


class AddItem(BaseModel):
    Name: str
    Price: float = Field(None, gt=0, description="The price must be greater than zero")
    Category: str

    class Config:
        orm_mode = True


class EditItem(BaseModel):
    Name: Optional[str] = None
    Price: Optional[float] = Field(None, gt=0, description="The price must be greater than zero")
    Category: Optional[str] = None

    class Config:
        orm_mode = True


''' ORDERS '''


class AddOrder(BaseModel):
    Comments: Optional[str] = None
    Email: Optional[str] = None

    class Config:
        orm_mode = True


class EditOrder(BaseModel):
    TotalPrice: Optional[int] = Field(None, ge=0, description="The total price must be greater than or equal to zero")
    Comments: Optional[str] = None
    Email: Optional[str] = None

    class Config:
        orm_mode = True


''' ORDEREDITEMS '''


class AddOrderedItem(BaseModel):
    MenuID: int
    OrderID: int
    Quantity: int = Field(..., gt=0, description="The quantity must be greater than zero")

    class Config:
        orm_mode = True


class EditOrderedItem(BaseModel):
    MenuID: Optional[int] = None
    OrderID: Optional[int] = None
    Quantity: int = Field(None, gt=0, description="The quantity must be greater than zero")
    UnitPrice: int = Field(None, gt=0, description="The unit price must be greater than zero")

    class Config:
        orm_mode = True
