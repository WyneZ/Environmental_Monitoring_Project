from app.db.crud import get_all


def register_device(device_info, user_id):
    # Save to 'devices' collection
    return True


def update_device_status(device_id, status):
    # Update status in MongoDB
    return True

async def get_devices_by_room(room_id: str):
    device_list: list = []
    devices = await get_all("devices_col")
    for device in devices:
        if str(device.get("room_id")) == room_id:
            device_list.append(device)
    print("Devices in room:", device_list)
    return device_list