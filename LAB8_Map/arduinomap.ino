#include <Servo.h>

Servo servo;

const int servoPin = 3;          // Servo control pin
const int trigPin = A5;           // Ultrasonic trigger pin
const int echoPin = A4;           // Ultrasonic echo pin

const int servoMinAngle = 0;     // Minimum servo angle
const int servoMaxAngle = 180;   // Maximum servo angle
const int step = 5;              // Step size for servo sweep
const unsigned long delayBetweenSteps = 100;  // Delay for servo to settle in ms

void setup() {
  Serial.begin(9600);
  servo.attach(servoPin);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

long readUltrasonicDistance() {
  // Send 10us pulse to trigger
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read echo time in microseconds
  long duration = pulseIn(echoPin, HIGH, 30000);  // timeout 30ms (max ~5m)

  // Calculate distance in cm (speed of sound = 343 m/s)
  long distanceCm = duration * 0.0343 / 2;

  if (duration == 0) {
    return -1;  // no echo received
  } else {
    return distanceCm;
  }
}

void loop() {
  // Sweep servo from 0 to 180 and back
  for (int angle = servoMinAngle; angle <= servoMaxAngle; angle += step) {
    servo.write(angle);
    delay(delayBetweenSteps);

    long distance = readUltrasonicDistance();

    // Send angle and distance as CSV string
    Serial.print(angle);
    Serial.print(",");
    Serial.println(distance);
  }

  for (int angle = servoMaxAngle; angle >= servoMinAngle; angle -= step) {
    servo.write(angle);
    delay(delayBetweenSteps);

    long distance = readUltrasonicDistance();

    Serial.print(angle);
    Serial.print(",");
    Serial.println(distance);
  }
}
