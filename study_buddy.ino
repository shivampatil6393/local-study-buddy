
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

const char* WIFI_SSID = "YOUR_WIFI";
const char* WIFI_PASSWORD = "YOUR_PASSWORD";

// Replace with your computer's local IPv4 address.
const char* SERVER =
"http://192.168.1.10:5000/api/esp32/status";

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

#define OLED_SDA 21
#define OLED_SCL 22
#define MOTOR_PIN 25

Adafruit_SSD1306 display(
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    &Wire,
    -1
);

unsigned long lastUpdate = 0;

void drawFace(String face, String message) {

    display.clearDisplay();
    display.setTextColor(SSD1306_WHITE);

    if (face == "happy") {

        display.fillCircle(42, 22, 4, WHITE);
        display.fillCircle(86, 22, 4, WHITE);

        display.drawLine(48, 40, 56, 45, WHITE);
        display.drawLine(56, 45, 72, 45, WHITE);
        display.drawLine(72, 45, 80, 40, WHITE);

    }

    else if (face == "thinking") {

        display.fillCircle(42, 22, 3, WHITE);
        display.drawCircle(86, 22, 5, WHITE);

        display.drawCircle(64, 40, 5, WHITE);

    }

    else {

        display.drawCircle(42, 22, 5, WHITE);
        display.drawCircle(86, 22, 5, WHITE);

        display.drawLine(53, 45, 64, 37, WHITE);
        display.drawLine(64, 37, 75, 45, WHITE);
    }

    display.setTextSize(1);
    display.setCursor(3, 53);

    display.print(message.substring(0, 20));

    display.display();
}


void connectWiFi() {

    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
    }
}


void updateBuddy() {

    if (WiFi.status() != WL_CONNECTED) {
        connectWiFi();
        return;
    }

    HTTPClient http;

    http.begin(SERVER);

    int code = http.GET();

    if (code == 200) {

        JsonDocument doc;

        deserializeJson(
            doc,
            http.getString()
        );

        String face = doc["face"] | "happy";
        String message = doc["message"] | "Ready!";

        bool vibrate = doc["vibrate"] | false;

        drawFace(face, message);

        if (vibrate) {

            digitalWrite(MOTOR_PIN, HIGH);
            delay(120);
            digitalWrite(MOTOR_PIN, LOW);

        }
    }

    http.end();
}


void setup() {

    pinMode(MOTOR_PIN, OUTPUT);

    digitalWrite(MOTOR_PIN, LOW);

    Wire.begin(OLED_SDA, OLED_SCL);

    display.begin(
        SSD1306_SWITCHCAPVCC,
        0x3C
    );

    connectWiFi();

    drawFace(
        "happy",
        "Study buddy online!"
    );
}


void loop() {

    if (millis() - lastUpdate >= 1500) {

        lastUpdate = millis();

        updateBuddy();

    }
}
