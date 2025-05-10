import motor.motor_asyncio
import asyncio

# Setup MongoDB client and collection
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://admin:admin@localhost:27017/")
db = client["ESP32_Datas"]
col = db["device_col"]

# Async function to delete all documents
async def delete_all_data():
    result = await col.delete_many({})  # Empty filter {} will delete all documents
    print(f"Deleted {result.deleted_count} documents.")

# Run the async function
if __name__ == "__main__":
    asyncio.run(delete_all_data())
