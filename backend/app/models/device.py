from pydantic import BaseModel
from typing import Optional


class Metadata(BaseModel):
    mac: str
    service_uuid: str


class Device(BaseModel):
    device_id: Optional[str] = None
    name: Optional[str] = None
    owner_id: Optional[str] = None
    room_id: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None
    last_seen: Optional[str] = None
    metadata: Metadata


class WiFiConfig(BaseModel):
    ssid: str
    password: str
    device_address: str
