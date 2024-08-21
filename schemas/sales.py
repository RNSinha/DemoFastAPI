# schemas/sales.py

from pydantic import BaseModel
from typing import Optional

class SalesCreate(BaseModel):
    product_name: str
    quantity: str
    price: float
    date: str



class SalesUpdate(BaseModel):
    product_name: Optional[str]
    quantity: Optional[str]
    price: Optional[str]
    date: Optional[str]

