from fastapi import APIRouter  # type: ignore
from ..models.room import Room
from app.db.crud import create, get_all, get_one, delete_one
from app.services.device_service import get_devices_by_room
from bson import ObjectId


router = APIRouter()

@router.get("/")
async def get_rooms():
    rooms: list = await get_all("rooms_col")
    print("Retrieved rooms:", rooms)
    return rooms

@router.post("/", response_model=Room)
async def create_room(room: Room):
    room_data = room.dict()
    result = await create("rooms_col", room_data)
    if result:
        print("Room created successfully:", room_data)
        return Room(**room_data)
    else:
        raise Exception("Failed to create room")
    
@router.get("/{id}")
async def get_room(id: str):
    room = await get_one("rooms_col", ObjectId(id))
    room["_id"] = str(room["_id"])
    if room:
        print("Room found:", room)
        device_list: list = await get_devices_by_room(id) or []
        print(f"room: {room}, devices: {device_list}")
        return {"room": room, "devices": device_list}
    else:
        raise Exception("Room not found")
    
@router.put("/{id}")
async def update_room(id: str, room: Room):
    room_data = room.dict()
    result = await create("rooms_col", room_data)

@router.delete("/{id}")
async def delete_room(id: str):
    result = await delete_one("rooms_col", ObjectId(id))
    if result:
        print(f"Room with id {id} deleted successfully.")
        return {"message": "Room deleted successfully."}
    else:
        raise Exception("Failed to delete room")
