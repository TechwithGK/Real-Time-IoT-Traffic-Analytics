#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>


const char* ssid = "Galaxysam99";     
const char* password = "**********";         
const char* serverEndpoint = "http://10.175.172.28:5000/api/log"; 

const int IR_PIN = 5;      // D1
const int BUZZER_PIN = 4;  // D2

bool objectDetected = false;
unsigned long breakStartTime = 0;

void setup() {
  Serial.begin(115200); 
  delay(1000);
  
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, HIGH); 

  Serial.print("Connecting to Wi-Fi: ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nCONNECTED SUCCESSFULLY! 🎉");
  Serial.print("NodeMCU IP Address: ");
  Serial.println(WiFi.localIP());

  pinMode(IR_PIN, INPUT);
}

void loop() {
  int sensorValue = digitalRead(IR_PIN);

  if (sensorValue == LOW && !objectDetected) {
    objectDetected = true;
    breakStartTime = millis();
    Serial.println("→ Object Detected!");
  } 
  else if (sensorValue == HIGH && objectDetected) {
    objectDetected = false;
    unsigned long breakDuration = millis() - breakStartTime;
    
    Serial.print("← Object Left. Duration: ");
    Serial.print(breakDuration);
    Serial.println(" ms");

    if (WiFi.status() == WL_CONNECTED) {
      WiFiClient client;
      HTTPClient http;
      
      http.begin(client, serverEndpoint);
      http.addHeader("Content-Type", "application/x-www-form-urlencoded");
      
      String httpRequestData = "duration_ms=" + String(breakDuration);
      int httpResponseCode = http.POST(httpRequestData);
      
      if (httpResponseCode > 0) {
        String response = http.getString();
        Serial.print("Server Response Code: ");
        Serial.println(httpResponseCode);
        if (response == "ALARM") {
          triggerAlarm(); 
        }
      } else {
        Serial.print("Network Error: ");
        Serial.println(httpResponseCode);
      }
      http.end();
    }
  }
  delay(50);
}

void triggerAlarm() {
  Serial.println("⚠️ DASHBOARD FLAGGED ANOMALY! BUZZER ON!");
  for(int i=0; i<3; i++) {
    digitalWrite(BUZZER_PIN, LOW);  // ON
    delay(200);
    digitalWrite(BUZZER_PIN, HIGH); // OFF
    delay(200);
  }
}