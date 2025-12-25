# FPGA-Accelerated Multi-Sensor Predictive-Maintenance Platform

An end-to-end Industrial IoT (IIoT) solution for real-time equipment monitoring and anomaly detection using Edge AI and custom FPGA hardware acceleration.

## 🚀 Key Features
* **Edge Intelligence:** ESP32 firmware using quantized **TensorFlow Lite (INT8)** for local anomaly detection.
* **Hardware Acceleration:** Custom **AXI4-Stream** Verilog IP core for offloading neural network matrix operations.
* **Real-time Dashboard:** **FastAPI** backend with **MQTT** integration for live telemetry streaming.
* **Production Verification:** Automated hardware-in-the-loop simulation using **Cocotb** and **Icarus Verilog**.

## 🛠 Tech Stack
* **Hardware:** Verilog HDL, Xilinx Vivado, ESP32 (C++).
* **AI/ML:** TensorFlow, TFLite (Post-Training Quantization).
* **Backend:** Python, FastAPI, MQTT (Mosquitto), SQLite.
* **Frontend:** HTML5, JavaScript, Tailwind CSS.

## 📁 Project Structure
* `backend/`: FastAPI server and MQTT subscriber.
* `dashboard/`: Web interface for real-time visualization.
* `fpga/`: AXI-Stream Verilog IP and build scripts.
* `firmware/`: ESP32 source code and TFLite model integration.
* `models/`: ML training and conversion pipeline.

## ⚡ Quick Start
1. **Start Backend:** `cd backend && uvicorn app.main:app`
2. **Start Dashboard:** `cd dashboard && python3 -m http.server 8080`
3. **Run Simulator:** `python3 simulator/simulate_nodes.py`

