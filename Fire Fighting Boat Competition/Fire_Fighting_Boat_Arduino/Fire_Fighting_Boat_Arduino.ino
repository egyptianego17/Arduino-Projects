#define enA 9        //Motor A enable
#define in1 7        //Motor A in1
#define in2 8        //Motor A in2
#define enB 3        //Motor B enable
#define in3 11       //Motor B in1
#define in4 10       //Motor B in2
#define PUMP 4       //Pump enable
#define BtStatus 2   // Bluetooth State Pin

//Expected incoming data from the serial

#define UP "U"   
#define UP_Right "Q"
#define UP_Left "W"
#define DOWN "D"
#define DOWN_Right "X"
#define DOWN_Left "Z"
#define Right "R"
#define Left "L"
#define Stop "S"
#define Fire "F"
#define Stop_Fire "f"
#define Speed_UP "I"
#define Speed_DOWN "J"

int speeds = 175;
int motorSpeedA = speeds; // MOTOR 1 SPEED
int motorSpeedB = speeds; // MOTOR 2 SPEED

String incomingByte; //For the coming string

#include <Servo.h>

Servo X;
Servo Y;
int time = 0;
void setup() {
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(PUMP, OUTPUT);
  pinMode(BtStatus, INPUT);
  X.write(posx);
  Y.write(posy);
  
  Serial.setTimeout(25);
  digitalWrite(PUMP, HIGH);
}



void loop() {
  if (digitalRead(BtStatus) == 1)
  {
    if (Serial.available() > 0) {
      // Setting intial speed for both motors
      analogWrite(enA, motorSpeedA); // Send PWM signal to motor A
      analogWrite(enB, motorSpeedB); // Send PWM signal to motor B
  
      // read the incoming byte:
      incomingByte = Serial.readStringUntil('\n');
      Serial.println(incomingByte);
  
      if (incomingByte == DOWN) {
        // Set Motor A backward
        digitalWrite(in1, LOW);
        digitalWrite(in2, HIGH);
        // Set Motor B backward
        digitalWrite(in3, LOW);
        digitalWrite(in4, HIGH);
      }
      else if (incomingByte == UP) {
        // Set Motor A forward
        digitalWrite(in1, HIGH);
        digitalWrite(in2, LOW);
        // Set Motor B forward
        digitalWrite(in3, HIGH);
        digitalWrite(in4, LOW);
      }
  
      else if (incomingByte == Right) {
        // Set Motor A backward
        digitalWrite(in1, LOW);
        digitalWrite(in2, HIGH);
        // Set Motor B forward
        digitalWrite(in3, HIGH);
        digitalWrite(in4, LOW);
  
      }
      else if (incomingByte == Left) {
        // Set Motor A forward
        digitalWrite(in1, HIGH);
        digitalWrite(in2, LOW);
        // Set Motor B backward
        digitalWrite(in3, LOW);
        digitalWrite(in4, HIGH);
  
      }
  
      else if (incomingByte == UP_Left) {
        // Set Motor A forward
        digitalWrite(in1, HIGH);
        digitalWrite(in2, LOW);
        // Stop Motor B
        digitalWrite(in3, LOW);
        digitalWrite(in4, LOW);
      }
      else if (incomingByte == UP_Right) {
        // Stop Motor A
        digitalWrite(in1, LOW);
        digitalWrite(in2, LOW);
        // Set Motor B forward
        digitalWrite(in3, HIGH);
        digitalWrite(in4, LOW);
      }
      else if (incomingByte == DOWN_Right) {
        // Stop Motor A
        digitalWrite(in1, LOW);
        digitalWrite(in2, LOW);
        // Set Motor B backward
        digitalWrite(in3, LOW);
        digitalWrite(in4, HIGH);
      }
      else if (incomingByte == DOWN_Left) {
        // Set Motor A backward
        digitalWrite(in1, LOW);
        digitalWrite(in2, HIGH);
        // Stop Motor B
        digitalWrite(in3, LOW);
        digitalWrite(in4, LOW);
      }
  
      // If joystick stays in middle the motors are not moving
      else if (incomingByte == Stop) {
        digitalWrite(in1, LOW);
        digitalWrite(in2, LOW);
        digitalWrite(in3, LOW);
        digitalWrite(in4, LOW);
      }
      // Motors Speed Control
      if ((incomingByte == Speed_UP) && (speeds <= 250 )) {
        speeds += 5 ;
        motorSpeedA = speeds; // MOTOR 1 SPEED
        motorSpeedB = speeds; // MOTOR 2 SPEED
      }
      else if ((incomingByte == Speed_DOWN) && (speeds >= 65)) {
        speeds -= 5 ;
        motorSpeedA = speeds; // MOTOR 1 SPEED
        motorSpeedB = speeds; // MOTOR 2 SPEED
      }
      //Start Firing
      if (incomingByte == Fire) {
        digitalWrite(PUMP, LOW);
      }
      //Stop Firing
      else if (incomingByte == Stop_Fire) {
        digitalWrite(PUMP, HIGH);
      }
    }
  }
  // If serial is not available then stop the motors and pump
  else 
  {
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);
    digitalWrite(PUMP,HIGH);
  }
}
