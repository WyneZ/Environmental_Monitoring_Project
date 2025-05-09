


from pydnatic import BaseModel

class SensorData(BaseModel):
    temperature: float
    humidity: float
    timestamp: str
