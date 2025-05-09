
import paho.mqtt.client as mqtt
import random
import time
import json

broker = "localhost"
port = 1883
topic = "randomNumber"

client = mqtt.Client()
client.connect(broker, port, 60)
client.loop_start()

try:
    while True:
        data = {
            "value": random.randint(1, 100)
        }
        client.publish(topic, json.dumps(data))
        print(f"Published: {data}")
        time.sleep(2)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
