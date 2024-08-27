# routers/sales.py
from fastapi import APIRouter, HTTPException
from models.sales import Sales
from schemas.sales import SalesCreate, SalesUpdate
from database import sales_collection
from bson import ObjectId

router = APIRouter()

@router.post("/sales", response_model=Sales)
async def create_sales(sales: SalesCreate):
    sales_dict = sales.dict()
    new_sales = await sales_collection.insert_one(sales_dict)
    sales_dict['_id'] = str(new_sales.inserted_id)
    return Sales(**sales_dict)

@router.get("/sales/{sales_id}", response_model=Sales)
async def get_sales(sales_id: str):
    sales = await sales_collection.find_one({"_id": ObjectId(sales_id)})
    if sales:
        sales['_id'] = str(sales['_id'])
        return Sales(**sales)
    raise HTTPException(status_code=404, detail="Sales record not found")


@router.get("/getSaleslist/")
async def get_saleslist():
    sales = []
    async for sale in sales_collection.find():
        sales.append(sales_helper(sale))
    
    return sales 
  

@router.put("/sales/{sales_id}", response_model=Sales)
async def update_sales(sales_id: str, sales: SalesUpdate):
    sales_dict = {k: v for k, v in sales.dict().items() if v is not None}
    updated_sales = await sales_collection.find_one_and_update(
        {"_id": ObjectId(sales_id)},
        {"$set": sales_dict},
        return_document=True
    )
    if updated_sales:
        updated_sales['_id'] = str(updated_sales['_id'])
        return Sales(**updated_sales)
    raise HTTPException(status_code=404, detail="Sales record not found")

@router.delete("/sales/{sales_id}")
async def delete_sales(sales_id: str):
    delete_result = await sales_collection.delete_one({"_id": ObjectId(sales_id)})
    if delete_result.deleted_count == 1:
        return {"message": "Sales record deleted successfully"}
    raise HTTPException(status_code=404, detail="Sales record not found")



def sales_helper(sale) -> dict:
    return {
        "id": str(sale["_id"]),
        "product_name": sale["product_name"],
        "quantity": sale["quantity"],
        "price": sale["price"],
        "date": sale["date"],    
    }