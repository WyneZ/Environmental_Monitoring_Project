from pydantic import BaseModel # type: ignore


class Room(BaseModel):
    room_name: str
    # owner_id: str
    devices_count: int = 0
    device_list: list = []
    last_updated: str = ""  

    class Config:
        from_attributes = True


        