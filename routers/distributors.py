# routers/distributors.py

from fastapi import FastAPI, HTTPException,APIRouter, status, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from models.distributors import Distributors
from database import distributor_collection
from fastapi.security import OAuth2PasswordBearer
from typing import Dict
from bson import ObjectId

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def raise_invalid_token_exception():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )

def raise_data_not_saved_exception():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Data not saved",
    )

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Replace this with your actual token validation logic
    if token != "fake-token":  # Replace this with your real token validation
        raise_invalid_token_exception()
    return {"sub": "user"}  # This is just an example, customize it as per your needs


def distributor_helper(distributor) -> dict:
    return {
        "id": str(distributor["_id"]),
        "sDistributorCode": distributor["sDistributorCode"],
        "sName": distributor["sName"],
        "sContactPerson": distributor["sContactPerson"],
        "sContactNo": distributor["sContactNo"],
        "sStreet": distributor["sStreet"],
        "sStreet2": distributor["sStreet2"],
        "sStreet3": distributor["sStreet3"],
        "sTown": distributor["sTown"],
        "sRegionName": distributor["sRegionName"],
        "sStateName": distributor["sStateName"],
        "sCity": distributor["sCity"],
        "sPinCode": distributor["sPinCode"],
        "sPaymentTerms": distributor["sPaymentTerms"],
        "sGSTNo": distributor["sGSTNo"],
        "sEmail": distributor["sEmail"],
        "sASMSAPCode": distributor["sASMSAPCode"],
        "sCustomerGroup": distributor["sCustomerGroup"],
        "sUserName": distributor["sUserName"],
        "sKey": distributor["sKey"],
    }




@router.post("/distributors/")
async def create_distributor(distributor: Distributors, current_user: Dict = Depends(get_current_user)):
    try:

    
        distributor_dict = distributor.dict(by_alias=True)

        if distributor.sDistributorCode == "":  # Example check
            raise_data_not_saved_exception()

        result = await distributor_collection.insert_one(distributor_dict)
        if result.inserted_id:
            return {"success": "Data saved successfully", "id": str(result.inserted_id), "user": current_user}
        raise HTTPException(status_code=400, detail="Error inserting data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/getdistributorslist/")
async def get_distributors(current_user: Dict = Depends(get_current_user)):
    distributors = []
    async for distributor in distributor_collection.find():
        distributors.append(distributor_helper(distributor))
    
    return distributors     


@router.get("/distributor/{id}")
async def get_distributor_by_id(id: str, current_user: Dict = Depends(get_current_user)):
    try:
        # Check if the provided ID is a valid ObjectId
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")

        # Find the distributor by ID
        distributor = await distributor_collection.find_one({"_id": ObjectId(id)})

        if distributor is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Distributor not found")

        return distributor_helper(distributor)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
