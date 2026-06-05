# 📊 Real-Time Spatial Traffic Analytics Dashboard & IoT Pipeline

An end-to-end Data Science & IoT pipeline that captures live physical world events, processes data streams via a local API, and visualizes system traffic with dynamic anomaly detection.

## 🚀 System Architecture
* **Edge Computing (Hardware):** NodeMCU (ESP8266) + IR Sensors capturing real-time object interaction intervals.
* **Data Engineering (Backend):** Flask API handling concurrent HTTP POST data streams and managing local data storage.
* **Statistical Analytics:** A rolling moving average algorithm ($avg\_duration \times 3$) running on the server side to instantly flag traffic anomalies.
* **Live UI (Frontend):** A high-fidelity Streamlit dashboard refreshing every 2 seconds to plot second-by-second time-series data and hourly density.

## 🛠️ Tech Stack
* **Languages:** Python, C++
* **Frameworks & Libraries:** Flask, Streamlit, Pandas
* **Hardware Core:** ESP8266 WiFi Module
