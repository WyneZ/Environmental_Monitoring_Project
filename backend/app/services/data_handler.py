from datetime import datetime
from app.db.mongodb import get_collectoin
from motor.motor_asyncio import AsyncIOMotorClient

mongo_client = AsyncIOMotorClient("mongodb://admin:admin@localhost:27017")
db = mongo_client["ESP32_Datas"]
data_col = db["dataCollection"]


async def handle_incoming_data(data):
    print("Started DB")
    if data_col is not None:
        data["timestamp"] = str(datetime.now())
        await data_col.insert_one(data)
        print("Stored in MongoDB:", data)
        data["_id"] = str(data["_id"])

        from app.main3 import sio
        await sio.emit("datas", data)
        print("Data Emitted")
    else:
        print("Error: MongoDB collection is not available.")
