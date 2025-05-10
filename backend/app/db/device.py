

from pymongo import MongoClient
from services.auth import hash_password

client = MongoClient("mongodb://localhost:27017")
db = client.iot_project
devices = db.devices

# Example: register a device
devices.insert_one({
    "device_id": "E422DA7C5824",
    "password": hash_password("pass123")
})
