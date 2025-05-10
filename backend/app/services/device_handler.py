from motor.motor_asyncio import AsyncIOMotorClient


client = AsyncIOMotorClient("mongodb://admin:admin@localhost:27017")
db = client["ESP32_Datas"]
col = db["device_col"]


async def handle_device(data):
    condition = await col.find_one({"device_id": data})
    print(f"<handle-device> Condition {condition}")
    print(f"<handle-device> {data}")
    print(type(condition))
    if condition:
        print(f"{data} is existed")
    else:
        print(f"Doesn't Exist")
        device_input = {"device_id": data}
        
        await col.insert_one(device_input)
        data["_id"] = str(data["_id"])
        print("Device Emitted")

    devices = []
    count = 0
    async for doc in col.find():
        devices.append(doc["device_id"])
        count += 1
    print(count)
    print(devices)
    
    
    from app.main3 import sio
    await sio.emit("devices", devices)

