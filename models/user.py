# models/user.py

from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class User(BaseModel):
    id: Optional[str] = Field(None, alias='_id')  # Map _id to id and make it optional
    email: EmailStr
    hashed_password: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
