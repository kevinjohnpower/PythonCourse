#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoOTA.h>

// Configure your Wi-Fi credentials.
const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// LED pin for most ESP32 dev boards.
constexpr uint8_t LED_PIN = 2;

// Blink delay in milliseconds (starts at 2 seconds).
volatile uint32_t blinkDelayMs = 2000;

WebServer server(80);

void handleRoot() {
  String message;
  message += "ESP32 Blink + OTA control\n";
  message += "Current delay (ms): ";
  message += String(blinkDelayMs);
  message += "\n\n";
  message += "Update delay with: /setDelay?ms=<value>\n";
  message += "Example: /setDelay?ms=500\n";
  server.send(200, "text/plain", message);
}

void handleSetDelay() {
  if (!server.hasArg("ms")) {
    server.send(400, "text/plain", "Missing 'ms' query parameter. Example: /setDelay?ms=2000");
    return;
  }

  const long requestedDelay = server.arg("ms").toInt();
  if (requestedDelay < 50 || requestedDelay > 600000) {
    server.send(400, "text/plain", "Delay must be between 50 and 600000 ms.");
    return;
  }

  blinkDelayMs = static_cast<uint32_t>(requestedDelay);

  String response = "Updated delay to ";
  response += String(blinkDelayMs);
  response += " ms";
  server.send(200, "text/plain", response);
}

void setupOTA() {
  ArduinoOTA.setHostname("esp32-blink");

  ArduinoOTA.onStart([]() {
    Serial.println("OTA update started.");
  });

  ArduinoOTA.onEnd([]() {
    Serial.println("\nOTA update finished.");
  });

  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
    Serial.printf("OTA Progress: %u%%\r", (progress * 100U) / total);
  });

  ArduinoOTA.onError([](ota_error_t error) {
    Serial.printf("OTA Error[%u]: ", error);
    if (error == OTA_AUTH_ERROR) {
      Serial.println("Auth Failed");
    } else if (error == OTA_BEGIN_ERROR) {
      Serial.println("Begin Failed");
    } else if (error == OTA_CONNECT_ERROR) {
      Serial.println("Connect Failed");
    } else if (error == OTA_RECEIVE_ERROR) {
      Serial.println("Receive Failed");
    } else if (error == OTA_END_ERROR) {
      Serial.println("End Failed");
    }
  });

  ArduinoOTA.begin();
  Serial.println("Arduino OTA ready.");
}

void connectToWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print('.');
  }

  Serial.println();
  Serial.print("Connected. IP address: ");
  Serial.println(WiFi.localIP());
}

void setupWebServer() {
  server.on("/", HTTP_GET, handleRoot);
  server.on("/setDelay", HTTP_GET, handleSetDelay);
  server.begin();
  Serial.println("HTTP server started.");
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);

  connectToWiFi();
  setupOTA();
  setupWebServer();
}

void loop() {
  static uint32_t lastToggle = 0;
  static bool ledState = false;

  const uint32_t now = millis();
  if (now - lastToggle >= blinkDelayMs) {
    ledState = !ledState;
    digitalWrite(LED_PIN, ledState ? HIGH : LOW);
    lastToggle = now;
  }

  server.handleClient();
  ArduinoOTA.handle();
}
