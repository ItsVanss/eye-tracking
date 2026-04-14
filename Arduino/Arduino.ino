char data;

int ledKanan = 10;
int ledTengah = 11;
int ledKiri = 12;

char lastData = 'X'; // untuk menghindari update berulang

void setup() {
  Serial.begin(9600);

  pinMode(ledKanan, OUTPUT);
  pinMode(ledTengah, OUTPUT);
  pinMode(ledKiri, OUTPUT);

  // Semua mati (active LOW)
  digitalWrite(ledKanan, HIGH);
  digitalWrite(ledTengah, HIGH);
  digitalWrite(ledKiri, HIGH);
}

void loop() {
  if (Serial.available() > 0) {
    data = Serial.read();

    // Hanya proses kalau data berubah
    if (data != lastData) {

      // Matikan semua dulu
      digitalWrite(ledKanan, HIGH);
      digitalWrite(ledTengah, HIGH);
      digitalWrite(ledKiri, HIGH);

      if (data == 'R') {
        digitalWrite(ledKanan, LOW);
      }
      else if (data == 'C') {
        digitalWrite(ledTengah, LOW);
      }
      else if (data == 'L') {
        digitalWrite(ledKiri, LOW);
      }

      lastData = data;
    }
  }
}