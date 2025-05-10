from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
import asyncio
from app.mqtt.publisher import esp_mqtt_client
from app.mqtt.subscriber import init_mqtt_subscriber
from app.db.mongodb import connect_to_mongo
# from app.api.routes import router as api_router

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = FastAPI()
sio_app = socketio.ASGIApp(sio, other_asgi_app=app)

loop = None

@app.on_event("startup")
async def startup_event():
    global loop
    loop = asyncio.get_event_loop()
    connect_to_mongo()
    init_mqtt_subscriber(loop)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Socket.IO Events
@sio.event
async def connect(sid, environ):
    print(f"<Subscriber> Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"<Subscriber> Client disconnected: {sid}")

@sio.on("send_to_esp32")
async def handle_send_to_esp32(sid, data):
    device_id = data.get("device_id")
    value = data.get("value")
    
    print(f"📦 Received for {device_id}: {value}")
    
    from app.mqtt.publisher import publish_to_esp32
    publish_to_esp32(data)


# === api/routes.py ===
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello world!"}
