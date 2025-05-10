import paho.mqtt.client as mqtt
import json

mqtt_topic_pub = "esp32/input"
esp_mqtt_client = mqtt.Client()
esp_mqtt_client.connect("localhost", 1883, 60)
esp_mqtt_client.loop_start()

def publish_to_esp32(data):
    mqtt_topic_spub = data.get("device_id") + "/input"
    result = esp_mqtt_client.publish(mqtt_topic_pub, json.dumps(data))
    if result[0] == 0:
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nPublisher:", data)
    else:
        print("Failed to send to ESP32")

