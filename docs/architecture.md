# System Architecture

The platform follows a distributed edge-computing architecture to minimize latency and optimize power consumption.

### Data Flow
1. **Data Acquisition:** ESP32 nodes (or simulators) sample vibration and temperature data.
2. **Edge Inference:** On-device TFLite models analyze the signal locally to detect immediate anomalies.
3. **Messaging:** Data is packaged into JSON and published via **MQTT** to the central broker.
4. **Ingestion & Acceleration:** The FastAPI backend subscribes to telemetry. When an anomaly is detected, complex analysis is offloaded to the **AXI4-Stream FPGA core**.
5. **Persistence & Visualization:** Processed data is stored in SQLite and served to the web dashboard via REST API.