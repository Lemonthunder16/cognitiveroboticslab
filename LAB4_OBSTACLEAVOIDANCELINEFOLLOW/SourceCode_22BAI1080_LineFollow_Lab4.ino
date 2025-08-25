#include <Servo.h>

// Motor driver pins
#define ENA 5   // Speed control for Motor A (Left)
#define ENB 6   // Speed control for Motor B (Right)
#define IN1 7   // Motor A direction
#define IN2 8
#define IN3 9   // Motor B direction
#define IN4 11

// Line sensor pins
#define LEFT 2
#define MID 4
#define RIGHT 10

void setup() {
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  pinMode(LEFT, INPUT);
  pinMode(MID, INPUT);
  pinMode(RIGHT, INPUT);
}


void loop() {
  int leftVal = digitalRead(LEFT);
  int midVal = digitalRead(MID);
  int rightVal = digitalRead(RIGHT);

  if (midVal == LOW) {          // Middle on black → go straight
    forward();
  } 
  else if (leftVal == LOW) {    // Left on black → turn left
    left();
  } 
  else if (rightVal == LOW) {   // Right on black → turn right
    right();
  } 
  else {                        // No sensor sees black → stop
    stopMotors();
  }
}

// ----- Motor functions -----
void forward() {
  analogWrite(ENA, 120);
  analogWrite(ENB, 120);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void left() {
  analogWrite(ENA, 200);
  analogWrite(ENB, 200);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void right() {
  analogWrite(ENA, 200);
  analogWrite(ENB, 200);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void stopMotors() {
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}
