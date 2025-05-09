

from motor.motor_asyncio import AsyncIOMotorClient

client = AsysncIOMotorClient("mongodb://admin:admin@localhost:27017")
db = client["ESP32_Datas"]
collection = db["dataCollection"]
