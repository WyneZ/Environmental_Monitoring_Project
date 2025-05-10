



import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import paho.mqtt.client as mqtt
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import json

from datetime import datetime

# Socket.IO server (ASGI mode)

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = FastAPI()
sio_app = socketio.ASGIApp(sio, other_asgi_app=app)


# Event loop for MQTT thread-safe operations
loop = None

@app.on_event("startup")
async def startup_event():
    global loop
    loop = asyncio.get_event_loop()

# MongoDB connection
mongo_client = AsyncIOMotorClient("mongodb://admin:admin@localhost:27017")
db = mongo_client["ESP32_Datas"]
collection = db["dataCollection"]

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set your frontend IP for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# List of connected Socket.IO clients is handled by `sio` automatically
mqtt_topic_sub = "esp32/datas"
mqtt_topic_pub = "esp32/input"

# Handle storing data and emitting to clients
async def store_and_emit(data):
    current_time = str(datetime.now())
    data["timestamp"] = current_time
    await collection.insert_one(data)
    print("Stored in MongoDB:", data)
    data["_id"] = str(data["_id"])  # Convert ObjectId
    await sio.emit("esp32_data", data)

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("MQTT connected.")
    client.subscribe(mqtt_topic_sub)

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print("MQTT Message received:", data)
    try:
        asyncio.run_coroutine_threadsafe(store_and_emit(data), loop)
    except Exception as e:
        print("Error storing data:", e)

# MQTT Client for receiving ESP32 sensor data
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

# MQTT Client for sending control data to ESP32
esp_mqtt_client = mqtt.Client()
esp_mqtt_client.connect("localhost", 1883, 60)
esp_mqtt_client.loop_start()

# Handle client connection
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

# Receive control data from frontend to send to ESP32
@sio.event
async def send_to_esp32(sid, data):
    print(f"Data from frontend to ESP32: {data}")
    result = esp_mqtt_client.publish(mqtt_topic_pub, data)
    if result[0] == 0:
        print("Sent to ESP32")
    else:
        print("Failed to send to ESP32")

@app.get("/")
async def root():
    return {"message": "Hello world!"}
