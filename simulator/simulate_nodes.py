# simulator/simulate_nodes.py
# Run with: python simulator/simulate_nodes.py
import time
import json
import random
import paho.mqtt.client as mqtt
from datetime import datetime

BROKER = "localhost"
TOPIC = "sensors/device_001/telemetry"

client = mqtt.Client()
client.connect(BROKER, 1883, 60)

print(f"Simulating ESP32 nodes publishing to {BROKER}...")

try:
    while True:
        # Simulate normal data vs anomaly (10% chance of anomaly)
        is_anomaly = random.random() > 0.90
        
        vibration = random.uniform(0.1, 0.5)
        if is_anomaly:
            vibration = random.uniform(2.5, 5.0) # Spike!

        payload = {
            "device_id": "device_001",
            "ts": datetime.now().isoformat(),
            "features": {
                "vibration_max": round(vibration, 4),
                "temp": round(random.uniform(40, 65), 1)
            },
            "anomaly": is_anomaly
        }

        client.publish(TOPIC, json.dumps(payload))
        print(f"Published: {payload['anomaly']} | Vib: {payload['features']['vibration_max']}")
        
        time.sleep(2) # Send data every 2 seconds
except KeyboardInterrupt:
    print("Simulation stopped.")