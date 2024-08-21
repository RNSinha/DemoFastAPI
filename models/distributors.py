# models/distributors.py

from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from bson import ObjectId
from typing import Any
from pydantic_core import core_schema

# MongoDB BSON ObjectId handler


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_json_schema__(cls, json_schema: dict, _field: Any) -> dict:
        json_schema.update(type="string")
        return json_schema

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Any) -> core_schema:
        return handler(source_type)

# Pydantic model for CustomerGroup
class CustomerGroup(BaseModel):
    CustomerGroupCode: str

# Pydantic model for the entire data structure
class Distributors(BaseModel):
   # id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    id: Optional[str] = Field(None, alias='_id')
    sDistributorCode: str
    sName: str
    sContactPerson: str
    sContactNo: str
    sStreet: str
    sStreet2: str
    sStreet3: str
    sTown: str
    sRegionName: str
    sStateName: str
    sCity: str
    sPinCode: str
    sPaymentTerms: str
    sGSTNo: str
    sEmail: EmailStr
    sASMSAPCode: str
    sCustomerGroup: List[CustomerGroup]
    sUserName: str
    sKey: str

    class Config:
        populate_by_name  = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
