

from pydantic import BaseModel


class ControlModel(BaseModel):
    control_id: str
    type: str
    pin: int
    status: str
    timestamp: str

class Control(BaseModel):
    device_id: str
    led: ControlModel