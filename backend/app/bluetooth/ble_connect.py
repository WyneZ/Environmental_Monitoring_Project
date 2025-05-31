from bleak import BleakClient
from bleak.exc import BleakError
import asyncio
from ..models.device import Metadata, Device


async def bluetooth_Connect(address: str, uuid_dict: dict):
    notification_future = asyncio.Future()
    wifiStatusChar = "42345678-5678-90ab-cdef-1234567890ab"
    service_uuid = None

    def notify_callback(sender, data: bytearray):
        data = data.decode('utf-8').strip().lower()
        print(f"📥 Notification from {sender}: {data}")
        if not notification_future.done():
            notification_future.set_result(data)

    async with BleakClient(address) as client:
        connected = client.is_connected
        if not connected:
            raise BleakError(f"Could not connect to device {address}")
        print("🔗 Connected!")
        services = client.services

        print("Discovered services:")
        for s in services:
            if service_uuid is None and s.uuid.startswith("00000000-0000-0000-0000-"):
                service_uuid = s.uuid
                
                print("Service UUID:", service_uuid)
        
        if service_uuid:
            await client.start_notify(wifiStatusChar, notify_callback)
            for uuid, value in uuid_dict.items():
                print(f"📡 Reading from {uuid}")                    
                if uuid.startswith("12345678"):
                    message = value
                    await client.write_gatt_char(uuid, message.encode())
                    print("Sent LED:", message)
                elif uuid.startswith("22345678"):
                    message = value
                    await client.write_gatt_char(uuid, message.encode())
                    print("Sent SSID:", message)
                elif uuid.startswith("32345678"):
                    message = value
                    await client.write_gatt_char(uuid, message.encode())
                    print("Sent Password:", message)
            print(f"42- {await notification_future}")
            await client.stop_notify(wifiStatusChar)
            return await notification_future
                    
        else:
            print("❌ Service UUID not found in device")
