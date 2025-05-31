

from pydantic import BaseModel


class Data(BaseModel):
    temperature: float
    humidity: float
    air_quality: int


class SensorData(BaseModel):
    device_id: str
    timestamp: str
    data: Data
