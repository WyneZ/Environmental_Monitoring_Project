

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import paho.mqtt.client as mqtt
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import json


app = FastAPI()

loop = None

@app.on_event("startup")
async def startup_event():
    global loop
    loop = asyncio.get_event_loop()


# MongoDB
mongo_client = AsyncIOMotorClient("mongodb://admin:admin@localhost:27017")
db = mongo_client["ESP32_Datas"]
collection = db["dataCollection"]


# CORS (For frontend on other OS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # specify frontend IP
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

websocket_clients = []
topic = "esp32/datas"


# MQTT 
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(topic)

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print("Received message:", data)
    
    try:
        result = asyncio.run_coroutine_threadsafe(store_in_mongo(data), loop).result()
    except Exception as e:
        print(f"Error storing data in MongoDB: {e}")


# Handle MongoDB and Send frontend using WebSocket
async def store_in_mongo(data):
    # Store data in MongoDB
    await collection.insert_one(data)
    print("Store Data:", data)
    
    # Send data to all connected WebSocket clients
    for ws in websocket_clients:
        print("Client is:", ws.client)
        data["_id"] = str(data["_id"])  # Convert ObjectId to string
        await ws.send_text(json.dumps(data))
    

# MQTT setup to send data to frontend
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
# mqtt_client.connect("host.docker.internal", 1883, 60)
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()


# WebSocket to send data to frontend
@app.websocket("/ws/get_data")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_clients.append(websocket)
    print("Client connected:", websocket.client)
    
    try:
        while True:
            data = await websocket.receive_text() # Keep the connection alive
            print("Received from client:", data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        websocket_clients.remove(websocket)
        print("Client disconnected:", websocket.client)


# MQTT setup to send data to ESP32
esp_mqtt_client = mqtt.Client()
# esp_mqtt_client.connect("192.168.110.172", 1883, 60) # Mosquitto running locally
# esp_mqtt_client.connect("mqtt-broker", 1883, 60)
esp_mqtt_client.connect("localhost", 1883, 60)
esp_mqtt_client.loop_start()


# WebSocket from Frontend
@app.websocket("/ws")
async def send_data_to_esp32(websocket: WebSocket):
    topic = "esp32/input"
    await websocket.accept()
    print("Client connected for ESP:", websocket.client)
    
    try:
        while True:
            data = await websocket.receive_text()
            print("Received from client:", data)
            result = esp_mqtt_client.publish(topic, data)  # Send data to ESP32
            status = result[0]
            if status == 0:
                print(f"Sent '{data}' to ESP32")
            else:
                print(f"Failed to send...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()
        print("Client disconnected:", websocket.client)


