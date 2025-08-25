#include <Servo.h>

// --- Pin Definitions ---
#define ENA 5
#define ENB 6
#define IN1 7
#define IN2 8
#define IN3 9
#define IN4 11

#define TRIG_PIN A5
#define ECHO_PIN A4
#define SERVO_PIN 3

// --- Constants ---
#define SAFE_DISTANCE 25   // cm - safety margin front
#define SIDE_MIN 18        // cm - keep away from side walls
#define SCAN_LEFT 150
#define SCAN_RIGHT 30
#define SCAN_CENTER 90

Servo ultrasonicServo;

void setup() {
  Serial.begin(9600);

  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  ultrasonicServo.attach(SERVO_PIN);
  ultrasonicServo.write(SCAN_CENTER);
  delay(500); 
}

void loop() {
  long forwardDist = getDistanceAt(SCAN_CENTER);

  if (forwardDist <= SAFE_DISTANCE && forwardDist > 0) {

    stopMotors();
    Serial.println("Obstacle ahead!");

    moveBackward(140);
    delay(250);
    stopMotors();
    delay(150);

    // Scan left and right
    long leftDist = getDistanceAt(SCAN_LEFT);
    delay(150);
    long rightDist = getDistanceAt(SCAN_RIGHT);
    delay(150);

    if (leftDist > rightDist && leftDist > SAFE_DISTANCE) {
      turnLeft(160);
      delay(400);
    } else if (rightDist > SAFE_DISTANCE) {
      turnRight(160);
      delay(400);
    } else {
      // Both sides blocked → reverse
      moveBackward(140);
      delay(600);
    }
    stopMotors();
    delay(150);
  } 
  else {
    long leftDist = getDistanceAt(SCAN_LEFT);
    long rightDist = getDistanceAt(SCAN_RIGHT);

    if (leftDist < SIDE_MIN) {
      // Too close to left wall → steer right slightly
      turnRight(160);
      delay(150);
    } 
    else if (rightDist < SIDE_MIN) {
      // Too close to right wall → steer left slightly
      turnLeft(160);
      delay(150);
    } 
    else {
      // Both sides okay → go straight
      moveForward(140);
      delay(300);   // small cautious step
    }

    stopMotors();
    delay(100);   // rescan often
  }
}

// --- Motor functions ---
void setMotorSpeed(int speedA, int speedB) {
  analogWrite(ENA, speedA);
  analogWrite(ENB, speedB);
}

void moveBackward(int speed) {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  setMotorSpeed(speed, speed);
}

void moveForward(int speed) {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  setMotorSpeed(speed, speed);
}

void turnRight(int speed) {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  setMotorSpeed(speed, speed);
}

void turnLeft(int speed) {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  setMotorSpeed(speed, speed);
}

void stopMotors() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  setMotorSpeed(0, 0);
}

// --- Distance functions ---
long getDistanceAt(int angle) {
  ultrasonicServo.write(angle);
  delay(200);
  return getDistance();
}

long getDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 20000);
  long distance = duration / 2 / 29.1;
  return distance;
}
