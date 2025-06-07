from fastapi import APIRouter # type: ignore
from typing import List
from bleak import BleakScanner # type: ignore
from ..models.device import Device, WiFiConfig, Metadata
from ..bluetooth.ble_connect import bluetooth_Connect
from app.utils.converters import str_to_bool
from app.db.crud import create, get_all, update_one


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
            print("Started Scan")
            metadata = Metadata(
                mac=str(d.address),
                service_uuid="unknown"
            )
            new_device = Device(name=d.name, metadata=metadata)
            all_devices = await get_all("devices_col")
            if all_devices == []:
                await create("devices_col", new_device.dict())
                print("No devices in database, creating new device:", metadata.mac)
            else:
                device_exist = False
                for device in all_devices:                    
                    if device["metadata"]["mac"] == metadata.mac:
                        print("Device already exists in database:", metadata.mac)
                        device_exist = True
                        break
                if not device_exist:
                    await create("devices_col", new_device.dict())
                    print("Device is created", metadata.mac)
            scanned_devices.append(new_device)
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
    if wifiStatus is True:
        wifi_data = {
            "ssid": config.ssid,
            "password": config.password,
            "device_address": config.device_address
        }
        for data in await get_all("wifi_config"):
            if data["device_address"] == config.device_address:
                await update_one("wifi_config", data["_id"], wifi_data)
                print("WiFi updated in database.")
                return {"success": True, "message": "Wi-Fi configuration updated."}
        await create("wifi_config", wifi_data)
        print("Wi-Fi configuration saved to database.")
    return {"success": wifiStatus}
