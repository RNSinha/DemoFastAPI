from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb+srv://sahajinfodelhi:HTXumrFEX9KPHTF1@cluster0.hqy76hs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = AsyncIOMotorClient(MONGO_DETAILS)

database = client.user_auth_db

user_collection = database.get_collection("users")
sales_collection = database.get_collection("sales")
distributor_collection = database.get_collection("distributor")


