from pydantic import BaseModel


class Room(BaseModel):
    room_name: str
    owner_id: str
    devices_count: int = 0
    last_updated: str = ""  

    class Config:
        orm_mode = True  # Enable ORM mode for compatibility with ORMs like SQLAlchemy