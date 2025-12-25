# FPGA-Accelerated Multi-Sensor Predictive-Maintenance Platform

An end-to-end Industrial IoT (IIoT) solution designed for real-time equipment monitoring and anomaly detection using Edge AI and custom FPGA hardware acceleration.

🚀 Key Features
* **Edge Intelligence:** ESP32 firmware utilizing quantized **TensorFlow Lite (INT8)** models for local, low-latency anomaly detection.
* **Hardware Acceleration:** Custom **AXI4-Stream** compliant Verilog IP core for offloading heavy matrix multiplication tasks.
* **Real-Time Monitoring:** High-performance **FastAPI** backend with **MQTT** integration for seamless telemetry streaming.
* **Proactive Alerting:** Live web dashboard providing instant visual feedback on sensor health and detected mechanical anomalies.
* **Production-Ready Verification:** Automated hardware-in-the-loop simulation using **Cocotb** and **Icarus Verilog**.

## 🛠 Tech Stack
* **Hardware:** Verilog HDL, Xilinx Vivado, ESP32 (C++/PlatformIO).
* **AI/ML:** TensorFlow, TFLite (Post-Training Quantization).
* **Backend:** Python, FastAPI, MQTT (Mosquitto), SQLite.
* **Frontend:** HTML5, JavaScript, Tailwind CSS.
* **DevOps:** GitHub Actions (CI), Pytest.

## 📋 Project Structure
* `backend/`: FastAPI server and MQTT subscriber logic.
* `dashboard/`: Responsive web interface for real-time visualization.
* `fpga/`: AXI-Stream Verilog IP core and Vivado build scripts.
* `firmware/`: ESP32 C++ source code and TFLite model integration.
* `host/`: Python bridge for FPGA hardware-software co-design.
* `models/`: Training scripts and model conversion pipeline.

## ⚡ Quick Start
1. **Start MQTT Broker:** `sudo service mosquitto start`
2. **Launch Backend:** `cd backend && uvicorn app.main:app`
3. **Launch Dashboard:** `cd dashboard && python3 -m http.server 8080`
4. **Run Simulator:** `python3 simulator/simulate_nodes.py`