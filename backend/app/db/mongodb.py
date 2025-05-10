

from motor.motor_asyncio import AsyncIOMotorClient


mongo_client = None
db = None
collectoion = None

def connect_to_mongo():
    global mongo_client, db, collection
    client = AsyncIOMotorClient("mongodb://admin:admin@localhost:27017")
    db = client["ESP32_Datas"]
    collection = db["dataCollection"]
    print("WTF Bro. I have been connected")


def get_collectoin():
    print("I give him to my collection.")
    if collection is None:
        raise RuntimeError("MongoDB collection is not initialized. Call connect_to_mongo() first.")
    return collection
