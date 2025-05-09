



from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import paho.mqtt.client as mqtt
from motor.motor_asyncio import AsyncIOMotorClient
import json
import asyncio
import random


app = FastAPI()

loop = None

@app.on_event("startup")
async def startup_event():
    global loop
    loop = asyncio.get_running_loop()


# MongoDB
mongo_client = AsyncIOMotorClient("mongodb://admin:admin@localhost:27017")
db = mongo_client["randomNumber_db"]
collection = db["randomNumber_data"]


# CORS (for frontend on other OS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify frontend IP
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

websocket_clients = []
topic = "randomNumber"


# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    client.subscribe(topic)

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print("\nReceived MQTT:", data)
    print(type(data))

    future = asyncio.run_coroutine_threadsafe(store_and_forward(data), loop)
    try:
        result = future.result()
        print("Result is ", result)
    except Exception as e:
        print("Coroutine failed:", e)
    


# Handle Mongo + WebSocket forwarding
async def store_and_forward(data):
    await collection.insert_one(data)
    print("Store Data: ", data)
    
    for ws in websocket_clients:
        print("Client is: ", ws.client)
        data["_id"] = str(data["_id"])
        await ws.send_json(data)
        print("Send Data: ", data)

# MQTT setup
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

# WebSocket route
@app.websocket("/ws/data")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep alive
    except:
        websocket_clients.remove(websocket)
