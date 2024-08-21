from fastapi import FastAPI
from routers import user, sales ,distributors

app = FastAPI()

app.include_router(user.router, prefix="/api/user", tags=["User"])
app.include_router(sales.router, prefix="/api/sales", tags=["Sales"])
app.include_router(distributors.router, prefix="/api/distributors", tags=["Distributors"])

@app.get("/")
def read_root():
    return {"Hello": "World"}




# from fastapi import FastAPI, HTTPException, Depends
# from passlib.context import CryptContext
# from models.user import User
# from schemas.user import UserCreate, UserLogin, ChangePassword
# from database import user_collection
# from pydantic import EmailStr

# app = FastAPI()

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def hash_password(password: str):
#     return pwd_context.hash(password)

# async def get_user(email: EmailStr):
#     user = await user_collection.find_one({"email": email})
#     if user:
#         user['_id'] = str(user['_id'])  # Convert ObjectId to string
#         return User(**user)
#     return None
    

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.post("/signup")
# async def signup(user: UserCreate):
#     existing_user = await get_user(user.email)
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
    
#     hashed_password = hash_password(user.password)
#     new_user = await user_collection.insert_one({
#         "email": user.email,
#         "hashed_password": hashed_password
#     })
#     return {"message": "User created successfully","id" : str(new_user.inserted_id)}

# @app.post("/login")
# async def login(user: UserLogin):
#     db_user = await get_user(user.email)
#     if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
#         raise HTTPException(status_code=400, detail="Invalid credentials")
    
#     return {"message": "Login successful"}

# @app.post("/change-password")
# async def change_password(data: ChangePassword):
#     db_user = await get_user(data.email)
#     if not db_user or not pwd_context.verify(data.old_password, db_user.hashed_password):
#         raise HTTPException(status_code=400, detail="Invalid credentials")
    
#     new_hashed_password = hash_password(data.new_password)
#     await user_collection.update_one({"email": data.email}, {"$set": {"hashed_password": new_hashed_password}})
#     return {"message": "Password updated successfully"}
