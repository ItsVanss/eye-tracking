#include <WiFi.h>

const char* ssid = "POCO F6";
const char* password = "vansvans";

WiFiServer server(1234);

int ledKanan = 2;
int ledTengah = 4;
int ledKiri = 5;

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("START");

  pinMode(ledKanan, OUTPUT);
  pinMode(ledTengah, OUTPUT);
  pinMode(ledKiri, OUTPUT);

  WiFi.begin(ssid, password);

  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nCONNECTED!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  server.begin();  // 🔥 PENTING BANGET
  Serial.println("SERVER STARTED");
}

void loop() {
  WiFiClient client = server.available();

  if (client) {
    Serial.println("Client Connected!");

    while (client.connected()) {
      if (client.available()) {
        char data = client.read();

        Serial.print("Data: ");
        Serial.println(data);

        // matikan semua
        digitalWrite(ledKanan, LOW);
        digitalWrite(ledTengah, LOW);
        digitalWrite(ledKiri, LOW);

        if (data == 'R') {
          digitalWrite(ledKanan, HIGH);
        }
        else if (data == 'C') {
          digitalWrite(ledTengah, HIGH);
        }
        else if (data == 'L') {
          digitalWrite(ledKiri, HIGH);
        }
      }
    }

    client.stop();
    Serial.println("Client Disconnected");
  }
}