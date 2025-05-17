# Environmental Monitoring Project

An integrated environmental monitoring system combining IoT sensors, a web-based dashboard, and backend services to collect, analyze, and visualize environmental data in real-time.

## 🌍 Overview

This project aims to provide a scalable and modular solution for environmental monitoring. It encompasses:

* **Firmware**: Embedded code for microcontrollers to collect sensor data.
* **Backend**: Server-side application to process and store incoming data.
* **Frontend**: Web interface for data visualization and user interaction.([GitHub][1], [GitHub][2])

## 🔧 Getting Started

### Prerequisites

* **Hardware**:

  * ESP32S3
  * DHT22, MQ135, LED
* **Software**:

  * FastAPI
  * MQTT(Mosquitto)
  * Arduino IDE (for firmware development)
  * MongoDB

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/WyneZ/Environmental_Monitoring_Project.git
   cd Environmental_Monitoring_Project
   ```

2. **Set up the backend**:

   * Navigate to the `backend` directory:

     ```bash
     cd backend
     ```
   * Install Python dependencies:

     ```bash
     pip install -r requirements.txt
     ```
   * Configure environment variables in the `.env` file.
   * Run the backend server:

     ```bash
     python app.py
     ```

3. **Set up the frontend**:

   * Navigate to the `frontend` directory:

     ```bash
     cd ../frontend
     ```
   * Install Node.js dependencies:

     ```bash
     npm install
     ```
   * Start the frontend application:

     ```bash
     npm start
     ```

4. **Deploy the firmware**:

   * Open the appropriate firmware file in the Arduino IDE.
   * Configure sensor pins and network settings as needed.
   * Upload the firmware to the microcontroller.

## 📊 Features

* **Real-time Data Collection**: Gather environmental data using various sensors.
* **Data Visualization**: Interactive graphs and charts to monitor environmental parameters.
* **Alerts & Notifications**: Set thresholds and receive alerts when values exceed limits.
* **Modular Design**: Easily extendable to incorporate additional sensors or functionalities.

## 📁 Documentation

Detailed documentation is available in the `docs` directory, including:

* **System Architecture**: Overview of the system's components and their interactions.
* **API Endpoints**: Descriptions of available backend APIs.
* **Sensor Calibration**: Guidelines for calibrating and validating sensor data.([GitHub][2])

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

