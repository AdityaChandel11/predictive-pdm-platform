# backend/app/main.py
import json
import threading
import time
import sys
import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import paho.mqtt.client as mqtt
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float
from sqlalchemy.orm import sessionmaker, declarative_base

# --- 1. Path Setup for FPGA Integration ---
# This allows the backend to find your host/fpga_client.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
try:
    from host.fpga_client import compute_on_fpga
    FPGA_AVAILABLE = True
except ImportError:
    FPGA_AVAILABLE = False
    print("Warning: host/fpga_client.py not found. FPGA simulation will be skipped.")

# --- 2. Database Setup (SQLite) ---
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
    fpga_processed = Column(Boolean, default=False) # Tracks if FPGA was used

Base.metadata.create_all(bind=engine)

# --- 3. MQTT & Hardware Acceleration Logic ---
MQTT_BROKER = "localhost"
MQTT_TOPIC = "sensors/+/telemetry"

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker (Result: {rc})")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        vibration = payload.get("features", {}).get("vibration_max", 0.0)
        is_anomaly = payload.get("anomaly", False)
        
        fpga_used = False
        # --- FPGA ACCELERATION TRIGGER ---
        if is_anomaly and FPGA_AVAILABLE:
            print(f"\n[ALERT] Anomaly on {payload.get('device_id')}! Offloading to FPGA...")
            # Simulate offloading to AXI-Stream Hardware
            # Using a fixed weight (0.85) for the hardware matrix multiplication
            fpga_result = compute_on_fpga(0.85, vibration)
            print(f"[FPGA Result] Signal analyzed: {fpga_result}")
            fpga_used = True
        
        # Save to Database
        db = SessionLocal()
        record = Telemetry(
            device_id=payload.get("device_id"),
            timestamp=payload.get("ts"),
            vibration_level=vibration,
            temperature=payload.get("features", {}).get("temp", 0.0),
            anomaly=is_anomaly,
            fpga_processed=fpga_used
        )
        db.add(record)
        db.commit()
        db.close()
    except Exception as e:
        print(f"Error processing message: {e}")

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

def start_mqtt():
    try:
        mqtt_client.connect(MQTT_BROKER, 1883, 60)
        mqtt_client.loop_forever()
    except Exception as e:
        print(f"MQTT Connection failed: {e}")

threading.Thread(target=start_mqtt, daemon=True).start()

# --- 4. FastAPI Endpoints ---
app = FastAPI(title="FPGA-Accelerated PdM Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {
        "status": "online", 
        "fpga_bridge": "connected" if FPGA_AVAILABLE else "disconnected",
        "mqtt": "listening"
    }

@app.get("/alerts")
def get_alerts(limit: int = 10):
    db = SessionLocal()
    alerts = db.query(Telemetry).filter(Telemetry.anomaly == True).order_by(Telemetry.id.desc()).limit(limit).all()
    db.close()
    return alerts

@app.get("/telemetry")
def get_telemetry(limit: int = 20):
    db = SessionLocal()
    data = db.query(Telemetry).order_by(Telemetry.id.desc()).limit(limit).all()
    db.close()
    return data