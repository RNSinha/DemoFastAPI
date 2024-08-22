# routers/user.py

from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from models.user import User
from schemas.user import UserLogin,UserCreate,ChangePassword
from database import user_collection
from pydantic import EmailStr
from bson import ObjectId


router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash_password(password: str):
    return pwd_context.hash(password)

async def get_user(email: EmailStr):
    user = await user_collection.find_one({"email": email})
    if user:
        user["id"] = str(user["_id"])
        return user   #(** user)
    return None


@router.post("/signup")
async def signup(user: UserCreate):
    existingUser = await get_user(user.email)
    if existingUser:
        raise HTTPException(status_code=400, detail= "Email already registered")
    

    hash_password = hash_password(user.password)
    new_user = await user_collection.insert_one({
        "email" : user.email,
        "hashed_password" : hash_password
    })

    return {"message" : "user Created Successfully", "id" : str(new_user.inserted_id) }


@router.post("/login")
async def login(user: UserLogin):
    db_user = await get_user(user.email)
    #if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
    if not db_user or not pwd_context.verify(user.password, db_user["hashed_password"]):  # Access dict keys correctly    
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    return {"message": "Login successful"}


@router.post("/change-password")
async def change_password(data: ChangePassword):
    db_user = await get_user(data.email)
    if not db_user or not pwd_context.verify(data.old_password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    new_hashed_password = hash_password(data.new_password)
    await user_collection.update_one({"email": data.email}, {"$set": {"hashed_password": new_hashed_password}})
    return {"message": "Password updated successfully"}
