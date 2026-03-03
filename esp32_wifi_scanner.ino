/*
  ESP32 Wi-Fi Scanner
  Upload with Arduino IDE and open Serial Monitor at 115200 baud.
*/

#include <WiFi.h>

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println();
  Serial.println("Starting ESP32 Wi-Fi scan...");

  // Put Wi-Fi in station mode and disconnect from any previous network.
  WiFi.mode(WIFI_STA);
  WiFi.disconnect(true, true);
  delay(100);
}

void loop() {
  Serial.println("Scanning for networks...");

  int networkCount = WiFi.scanNetworks();

  if (networkCount == 0) {
    Serial.println("No Wi-Fi networks found.");
  } else {
    Serial.printf("Found %d network(s):\n", networkCount);

    for (int i = 0; i < networkCount; i++) {
      Serial.printf(
        "%2d: SSID: %-32s | RSSI: %4d dBm | Channel: %2d | Encryption: %s\n",
        i + 1,
        WiFi.SSID(i).c_str(),
        WiFi.RSSI(i),
        WiFi.channel(i),
        (WiFi.encryptionType(i) == WIFI_AUTH_OPEN) ? "Open" : "Secured"
      );
    }
  }

  Serial.println();
  delay(5000); // Scan every 5 seconds
}
