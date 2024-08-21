# models/sales.py

from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional

class Sales(BaseModel):
    id : Optional[str] = Field(None, alias="_id")
    product_name: str
    quantity: int
    price: float
    date: str


    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}