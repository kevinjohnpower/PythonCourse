# ESP32 Blink with OTA Delay Update

This sketch blinks the onboard LED with a default delay of **2000 ms** and supports over-the-air updates in two ways:

1. **Runtime delay update over Wi-Fi** via HTTP endpoint.
2. **Firmware OTA update** via `ArduinoOTA`.

## Requirements

- ESP32 board support in Arduino IDE / PlatformIO
- Libraries:
  - `WiFi.h`
  - `WebServer.h`
  - `ArduinoOTA.h`

## Setup

1. Open `esp32_blink_ota.ino`.
2. Set your Wi-Fi credentials:
   - `WIFI_SSID`
   - `WIFI_PASSWORD`
3. Upload once over USB.
4. Open Serial Monitor at `115200` baud and note the board IP address.

## Update delay over the air (runtime)

In a browser on the same network:

- View status: `http://<esp32-ip>/`
- Set delay: `http://<esp32-ip>/setDelay?ms=2000`

Allowed range is 50 to 600000 ms.

## OTA firmware updates

After initial USB upload, use Arduino IDE network port (`esp32-blink`) to upload new firmware wirelessly.
