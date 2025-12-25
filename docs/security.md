# Security Implementation

## 1. MQTT Security (MQTTS)
* **Encryption:** In production, we use Port 8883 with SSL/TLS certificates.
* **Authentication:** The Mosquitto broker is configured with a `password_file` so only authorized ESP32 nodes can publish data.

## 2. API Security
* **HTTPS:** FastAPI is wrapped in Uvicorn with SSL keyfile and certfile.
* **CORS:** Currently set to `*` for development but restricted to the dashboard's IP in production.