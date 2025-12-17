# backend/app/main.py
# Run with: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
import json
import threading
import time
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import paho.mqtt.client as mqtt
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float
from sqlalchemy.orm import sessionmaker, declarative_base

# --- 1. Database Setup (SQLite) ---
DATABASE_URL = "sqlite:///./pdm_platform.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Telemetry(Base):
    __tablename__ = "telemetry"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    timestamp = Column(String)
    vibration_level = Column(Float)
    temperature = Column(Float)
    anomaly = Column(Boolean)

Base.metadata.create_all(bind=engine)

# --- 2. MQTT Setup (The Listener) ---
MQTT_BROKER = "localhost"
MQTT_TOPIC = "sensors/+/telemetry"

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f"Received: {payload}")
        
        # Save to DB
        db = SessionLocal()
        record = Telemetry(
            device_id=payload.get("device_id"),
            timestamp=payload.get("ts"),
            vibration_level=payload.get("features", {}).get("vibration_max", 0.0),
            temperature=payload.get("features", {}).get("temp", 0.0),
            anomaly=payload.get("anomaly", False)
        )
        db.add(record)
        db.commit()
        db.close()
    except Exception as e:
        print(f"Error processing message: {e}")

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Start MQTT in a background thread so it doesn't block the API
def start_mqtt():
    try:
        mqtt_client.connect(MQTT_BROKER, 1883, 60)
        mqtt_client.loop_forever()
    except Exception as e:
        print(f"MQTT Connection failed: {e}")

threading.Thread(target=start_mqtt, daemon=True).start()

# --- 3. FastAPI App (The API) ---
app = FastAPI(title="FPGA PDM Platform")

# Allow the dashboard (HTML) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "online", "db": "connected", "mqtt": "listening"}

@app.get("/alerts")
def get_alerts(limit: int = 10):
    db = SessionLocal()
    # Fetch records where anomaly is True
    alerts = db.query(Telemetry).filter(Telemetry.anomaly == True).order_by(Telemetry.id.desc()).limit(limit).all()
    db.close()
    return alerts

@app.get("/telemetry")
def get_telemetry(limit: int = 20):
    db = SessionLocal()
    data = db.query(Telemetry).order_by(Telemetry.id.desc()).limit(limit).all()
    db.close()
    return data