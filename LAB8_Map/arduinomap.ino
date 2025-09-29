#include <Servo.h>

Servo myServo;

const int trigPin = 9;     // HC-SR04 TRIG pin
const int echoPin = 10;    // HC-SR04 ECHO pin
const int servoPin = 3;    // Servo control pin

int servoMin = 0;          // Minimum servo angle
int servoMax = 180;        // Maximum servo angle
int step = 1;              // Servo step

void setup() {
  Serial.begin(9600);
  myServo.attach(servoPin);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

long readDistanceCM() {
  // Send trigger pulse
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read echo pulse
  long duration = pulseIn(echoPin, HIGH, 30000); // timeout 30ms (~5m)
  if (duration == 0) return -1; // no reading

  long distance = duration * 0.034 / 2; // cm
  return distance;
}

void loop() {
  // Sweep servo from 0 to 180
  for (int angle = servoMin; angle <= servoMax; angle += step) {
    myServo.write(angle);
    delay(15); // allow servo to move

    long distance = readDistanceCM();
    Serial.print(angle);
    Serial.print(",");
    Serial.println(distance);
    delay(50); // small delay to avoid flooding
  }

  // Optional: sweep back from 180 to 0
  for (int angle = servoMax; angle >= servoMin; angle -= step) {
    myServo.write(angle);
    delay(15);

    long distance = readDistanceCM();
    Serial.print(angle);
    Serial.print(",");
    Serial.println(distance);
    delay(50);
  }
}
