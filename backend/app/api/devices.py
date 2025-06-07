from fastapi import APIRouter  # type: ignore
from ..models.device import Device, Metadata
from app.db.crud import create, get_all, get_one


router = APIRouter()

@router.get("/")
async def get_devices():
    devices: list = await get_all("devices_col")
    print("Retrieved devices:", devices)
    return devices

@router.get("/{device_id}", response_model=Device)
async def get_device(device_id: str):
    device = await get_one("devices_col", device_id)
    if device:
        print("Device found:", device)
        return Device(**device)
    else:
        raise Exception(f"Device with ID {device_id} not found")

@router.post("/", response_model=Device)
async def create_device(device: Device):
    device_data = device.dict()
    result = await create("devices_col", device_data)
    if result:
        print("device created successfully:", device_data)
        return device(**device_data)
    else:
        raise Exception("Failed to create device")
    

    
