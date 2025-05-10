from datetime import datetime
from app.db.mongodb import get_collectoin
from motor.motor_asyncio import AsyncIOMotorClient

mongo_client = AsyncIOMotorClient("mongodb://admin:admin@localhost:27017")
db = mongo_client["ESP32_Datas"]
collection = db["dataCollection"]


async def handle_incoming_data(data):
    print("Started DB")
    # collection = get_collection()
    print("COllection gets.")
    if collection is not None:
        data["timestamp"] = str(datetime.now())
        await collection.insert_one(data)
        print("Stored in MongoDB:", data)
        data["_id"] = str(data["_id"])

        from app.main3 import sio
        print("Before emit")
        await sio.emit("esp32_data", data)
        print("Emitted")
    else:
        print("Error: MongoDB collection is not available.")
