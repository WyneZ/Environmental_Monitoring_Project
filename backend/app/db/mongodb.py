from motor.motor_asyncio import AsyncIOMotorClient # type: ignore
from app.config import settings


MONGO_URI = settings.MONGO_URI
MONGO_DB = settings.MONGO_DB

mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client[MONGO_DB]


def get_collection(name: str):
    return db[name]

def change_IdToStr(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

