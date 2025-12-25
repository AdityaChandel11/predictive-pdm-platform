/* firmware/esp32/src/main.cpp 
   Purpose: Read vibration, run TFLite inference, publish via MQTT
*/
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/schema/schema_generated.h"

// --- Configuration ---
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* mqtt_server = "YOUR_WSL_IP_ADDRESS"; // Use 'hostname -I' in WSL to find this

WiFiClient espClient;
PubSubClient client(espClient);

// TFLite globals
const tflite::Model* model = nullptr;
tflite::MicroInterpreter* interpreter = nullptr;
TfLiteTensor* input = nullptr;
TfLiteTensor* output = nullptr;
constexpr int kTensorArenaSize = 2 * 1024;
uint8_t tensor_arena[kTensorArenaSize];

void setup_wifi() {
    delay(10);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) { delay(500); }
}

void setup_tflite() {
    // In a real setup, we would include the "model.tflite" converted to a C array
    // For this portfolio code, we initialize the interpreter structure
    static tflite::MicroErrorReporter micro_error_reporter;
    static tflite::AllOpsResolver resolver;
    // model = tflite::GetModel(your_model_c_array); 
}

void publish_telemetry(float vibration, bool is_anomaly) {
    StaticJsonDocument<200> doc;
    doc["device_id"] = "esp32_node_01";
    doc["ts"] = "2025-12-26T00:00:00Z"; // In production, use NTP time
    doc["features"]["vibration_max"] = vibration;
    doc["anomaly"] = is_anomaly;

    char buffer[256];
    serializeJson(doc, buffer);
    client.publish("sensors/esp32_node_01/telemetry", buffer);
}

void setup() {
    Serial.begin(115200);
    setup_wifi();
    client.setServer(mqtt_server, 1883);
    setup_tflite();
}

void loop() {
    if (!client.connected()) { /* reconnect logic */ }
    client.loop();

    // 1. Simulate reading sensor
    float raw_vibration = analogRead(34) * (5.0 / 4095.0); 

    // 2. Run Inference (Simplified for MVP)
    // In a full build, you'd do: input->data.f[0] = raw_vibration; interpreter->Invoke();
    bool anomaly = (raw_vibration > 2.5); 

    // 3. Send to Backend
    publish_telemetry(raw_vibration, anomaly);
    
    delay(2000);
}