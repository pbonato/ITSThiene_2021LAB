#include <WiFi.h>
#include <HTTPClient.h>
#include <analogWrite.h>
#include <ArduinoJson.h>

#define LED_RED 32
#define LED_GREEN 33
#define LED_BLUE 25
#define DEBUG

const char* ssid = "TCPBerry_2.4";
const char* password =  "Vmware1!";
const char* serverName = "http://46.105.235.75:3000/api/get/98:54:1b:2a:1c:91";

unsigned long lastTime = 0;
unsigned long timerDelay = 40;

void setup(){
  #ifdef DEBUG
    Serial.begin(9600);
    while(!Serial.available()){;;}
  #endif
  WiFi.begin(ssid, password);
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_BLUE, OUTPUT);
}

void loop() {
  if ((millis() - lastTime) > timerDelay) {
    
    //Check WiFi connection status
    if(WiFi.status() == WL_CONNECTED){
      HTTPClient http;

      http.begin(serverName);
      
      http.addHeader("Content-Type", "application/json");

      if(http.GET() == 200){
        String json = http.getString();
        StaticJsonDocument<256> doc;
        
        DeserializationError error = deserializeJson(doc, json);
        // Test if parsing succeeds.
        if (error) {
          #ifdef DEBUG
          Serial.print(F("deserializeJson() failed: "));
          Serial.println(error.f_str());
          #endif
          return;
        }

        #ifdef DEBUG
        Serial.println("Get received!");
        bool mac = doc["mac"];
        int red = doc["red"];
        int green = doc["green"];
        int blue = doc["blue"];
        Serial.println("mac= " + mac + "\n" + "red= " + red + "\n" + "green= " + green + "\n" + "blue= " + blue + "\n--------");
        #endif

        digitalWrite(LED_RED, doc["red"]);
        digitalWrite(LED_GREEN, doc["green"]);
        digitalWrite(LED_BLUE, doc["blue"]);
      }
    }
    else {
      #ifdef DEBUG
      Serial.println("WiFi Disconnected");
      #endif
    }
    lastTime = millis();
  }
}
