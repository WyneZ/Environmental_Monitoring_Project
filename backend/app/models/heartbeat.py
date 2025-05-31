

from pydantic import BaseModel


class Heartbeat(BaseModel):
    device_id: str
    timestamp: str
    status: str 