from fastapi import APIRouter
from typing import List
from bleak import BleakScanner
from ..models.device import Device, WiFiConfig, Metadata
from ..bluetooth.ble_connect import bluetooth_Connect
from app.utils.converters import str_to_bool


router = APIRouter()

LED_UUID = "12345678-5678-90ab-cdef-1234567890ab"
SSID_UUID = "22345678-5678-90ab-cdef-1234567890ab"
PW_UUID = "32345678-5678-90ab-cdef-1234567890ab"

@router.get("/scan", response_model=List[Device])
async def scan_devices():
    scanned_devices = []
    devices = await BleakScanner.discover()
    for d in devices:
        if d.name and d.name.startswith("ESP32"):
            metadata = Metadata(
                mac=str(d.address),
                service_uuid=d.metadata.get("service_uuid", "Unknown")
            )
            device = Device(name=d.name, metadata=metadata)
            scanned_devices.append(device)
    print("Scanned devices:", scanned_devices)
    return scanned_devices

@router.post("/connect/{address}")
async def connecting_device(address: str):
    uuid_dict = {LED_UUID: "ON"}
    await bluetooth_Connect(address, uuid_dict)
    return {"message": "Welcome to the BLE Scanner API!"}

@router.post("/setup_wifi")
async def setup_wifi(config: WiFiConfig):
    uuid_dict = {SSID_UUID: config.ssid, PW_UUID: config.password, LED_UUID: "OFF"}
    print(uuid_dict)
    wifiStatus = str_to_bool(await bluetooth_Connect(config.device_address, uuid_dict))
    print(f"Wi-Fi setup for {config.device_address} - SSID={config.ssid}")
    print(f"Wi-Fi status: {wifiStatus}")
    return {"success": wifiStatus}
