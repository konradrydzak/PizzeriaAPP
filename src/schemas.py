from typing import Optional

from pydantic import BaseModel


class AddItem(BaseModel):
    Name: str
    Price: float
    Category: str

    class Config:
        orm_mode = True


class EditItem(BaseModel):
    Name: Optional[str] = None
    Price: Optional[float] = None
    Category: Optional[str] = None

    class Config:
        orm_mode = True
