import paho.mqtt.client as mqtt

mqtt_topic_pub = "esp32/input"
esp_mqtt_client = mqtt.Client()
esp_mqtt_client.connect("localhost", 1883, 60)
esp_mqtt_client.loop_start()

def publish_to_esp32(data):
    result = esp_mqtt_client.publish(mqtt_topic_pub, data)
    if result[0] == 0:
        print("Sent to ESP32")
    else:
        print("Failed to send to ESP32")

