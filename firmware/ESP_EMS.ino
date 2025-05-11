#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <time.h>


#define DHTPIN 11        
#define DHTTYPE DHT22
#define MQ135_PIN 4      
#define LED 2

// To Connect WiFi
const char* ssid = "NCC_InstituteOfScience";
const char* password = "CrazySci3ntist";
const char* mqtt_server = "192.168.110.172"; // IP of your Raspberry Pi

WiFiClient espClient;
PubSubClient client(espClient);
DHT dht(DHTPIN, DHTTYPE);

// Non-blocking timer
unsigned long lastSensorRead = 0;
const long sensorInterval = 10000;


String getID() {
  uint64_t chipid = ESP.getEfuseMac();  // 64-bit unique ID
  char chipString[17];
  sprintf(chipString, "%012llX", chipid);
  String deviceID = String(chipString);
  return deviceID;
}

String device_id = getID();


void ledControl(char* topic, byte* payload, unsigned int length) {
  // Convert payload to a string
  char message[length + 1];
  memcpy(message, payload, length);
  message[length] = '\0';

  // Create JSON document
  StaticJsonDocument<200> doc;
  DeserializationError error = deserializeJson(doc, message);

  if (error) {
    Serial.print("JSON parse failed: ");
    Serial.println(error.c_str());
    return;
  }

  const char* device = doc["device_id"];
  const char* value = doc["value"];

  Serial.print("Device ID: ");
  Serial.println(device_id);
  Serial.print("Value: ");
  Serial.println(value);

  if (strcmp(device, device_id.c_str()) == 0) {
    if(strcmp(value, "ON") == 0) {
        digitalWrite(LED, HIGH);
    }
    else {
      digitalWrite(LED, LOW);
    }
  } 
}


void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to WiFi ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
}


void reconnect() {
  while (!client.connected()) {
    Serial.print("Connecting to MQTT...");
    String clientId = "ESP32Client-" + getID();
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");

      client.subscribe("esp32/input"); // For LED control
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
    }
  }
}


void readSensorData() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  int mq135Value = analogRead(MQ135_PIN);

  StaticJsonDocument<200> doc;

  // Add sensor data to the JSON object
  doc["device_id"] = device_id;
  doc["temperature"] = temperature;
  doc["humidity"] = humidity;
  doc["air_quality"] = mq135Value;

  // Check LED status
  if(digitalRead(LED) == HIGH) {
    doc["LED_status"] = "ON";
  }
  else if (digitalRead(LED) == LOW) {
    doc["LED_status"] = "OFF";
  }

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT22 sensor!");
  } else {
      // Serialize JSON to string
      char output[256];
      serializeJson(doc, output);

      // Print JSON to Serial Monitor
      Serial.print("From ");
      Serial.println(getID());
      Serial.println("Publishing JSON to MQTT:");
      Serial.println(output);  // This prints the JSON string to the serial monitor
      
      // Publish the JSON string to MQTT
      String topic = device_id + "/datas";
      client.publish(topic.c_str(), output);
  }
}


void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
  dht.begin();
  setup_wifi();

  client.setServer(mqtt_server, 1883);
  client.setCallback(ledControl);

  Serial.println("ESP32 with DHT22 and MQ135 initialized");
}


void loop() {
  if (!client.connected()) {
    reconnect();
  }
  // readSensorData();
  client.loop();

  unsigned long now = millis();
  if (now - lastSensorRead >= sensorInterval) {
    lastSensorRead = now;
    readSensorData();
  }
  
}
