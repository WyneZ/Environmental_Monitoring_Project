import paho.mqtt.client as mqtt
import json
import asyncio
from app.services.data_handler import handle_incoming_data
from app.services.device_handler import handle_device

mqtt_topic_sub = "+/datas"
mqtt_client = mqtt.Client()
loop = None

def on_connect(client, userdata, flags, rc):
    print("MQTT connected.")
    client.subscribe(mqtt_topic_sub)

def on_message(client, userdata, msg):
    topic = msg.topic
    data = json.loads(msg.payload.decode())
    device_id = topic.split('/')[0]
    print(f"MQTT Message received from {device_id}: {data}")
    print(type(device_id))
    
    try:
        asyncio.run_coroutine_threadsafe(handle_device(device_id), loop)
        asyncio.run_coroutine_threadsafe(handle_incoming_data(data), loop)
    except Exception as e:
        print("Error storing data:", e)

async def disconnect(sid):
    print(f"Client {sid} disconnected")

def init_mqtt_subscriber(event_loop):
    global loop
    loop = event_loop
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect("localhost", 1883, 60)
    mqtt_client.loop_start()
