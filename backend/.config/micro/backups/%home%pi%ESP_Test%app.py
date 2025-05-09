


from fastapi import FastAPI, WebSocket
import paho.mqtt.client as mqtt
import asyncio

app = FastAPI()

mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)  # Mosquitto running locally
mqtt_client.loop_start() # This is imports

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received from frontend: {data}")
            # mqtt_client.publish("esp32/input", data)
            result = mqtt_client.publish("esp32/input", data)
            status = result[0]
            
            if status == 0:
                print(f"Sent `{data}` to topic `esp32/input`")
            else:
                print(f"Failed to send message to topic esp32/input")
            
    except Exception as e:
        print("WebSocket disconnected:", e)
        
