from .mongodb import get_collection, change_IdToStr
from bson import ObjectId # type: ignore


async def create(collection_name: str, data: dict):
    collection = get_collection(collection_name)
    result = await collection.insert_one(data)
    return result

async def update_one(collection_name: str, id: str, data: dict):
    collection = get_collection(collection_name)
    result = await collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.modified_count == 1:
        return True
    return False

async def get_one(collection_name: str, id: str):
    collection = get_collection(collection_name)
    doc = await collection.find_one({"_id": ObjectId(id)})
    if doc:
        print(doc, "found")
        return doc
    print(doc, "not found")
    return doc

async def get_all(collection_name: str):
    collection = get_collection(collection_name)
    cursor = collection.find({})
    data_list: list = []
    async for data in cursor:
        data["_id"] = str(data["_id"])
        data_list.append(data)
    return data_list

async def get_all_id(collection_name: str):
    collection = get_collection(collection_name)
    cursor = collection.find({})
    id_list = []
    async for doc in cursor:
        id = change_IdToStr(doc)
        id_list.append(id)
    return id_list

async def delete_one(collection_name: str, id: str):
    collection = get_collection(collection_name)
    result = await collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return True
    return False