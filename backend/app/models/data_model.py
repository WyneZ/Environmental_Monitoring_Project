


from pydnatic import BaseModel

class SensorData(BaseModel):
    device_id: str
    temperature: float
    humidity: float
    timestamp: str


class DeviceLogin(BaseModel):
    device_id: str
    password: str
