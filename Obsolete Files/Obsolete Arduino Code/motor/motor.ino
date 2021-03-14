// Import wire library to be able to use i2c communicaiton
#include <Wire.h>

// Define slave address
#define SLAVE_ADDR 9

// Define the motor control pins
#define mtrPwm1 9
#define mtrDir1 11
#define mtrPwm2 10
#define mtrDir2 12

// Initialize newData flag
boolean newData = false;

// Initialize motor command array that stores values read from bus
int mtrCmd[3];

// Motor 1 turns faster than motor 2, so add an offset to motor 1 speed commands to help the bot drive straight
int offset = 10;
void setup() {
  // Initialize motor pins
  pinMode(mtrPwm1, OUTPUT);
  pinMode(mtrDir1, OUTPUT);
  pinMode(mtrPwm2, OUTPUT);
  pinMode(mtrDir2, OUTPUT);

  // Initialize I2C communications as slave
  Wire.begin(SLAVE_ADDR);
  // Tell slave which function to run when receiving data from bus (motor input command function)
  Wire.onReceive(receiveEvent);
    
  // To be able to look at serial monitor when running code for test
  Serial.begin(9600);
}

void receiveEvent(int howMany) {
  while (Wire.available()) { // loop through all but the last
    for(int i = 0; i < 3; i++){
      mtrCmd[i] = Wire.read();
    }
  }
  newData = true;
}

void mtrCtrl(int speedFreq, int direction){
  switch (direction) {
    // Motors off
    case 0:
      analogWrite(mtrPwm1, 0);
      analogWrite(mtrPwm1, 0);
      break;
    // Move forward
    case 1:
      digitalWrite(mtrDir1, LOW);
      digitalWrite(mtrDir2, HIGH);
      break;
    // Move backwards
    case 2:
      digitalWrite(mtrDir1, HIGH);
      digitalWrite(mtrDir2, LOW);
      break;
    // Move left
    case 3:
      digitalWrite(mtrDir1, LOW);
      digitalWrite(mtrDir2, LOW);
      break;
    // Move right
    case 4:
      digitalWrite(mtrDir1, HIGH);
      digitalWrite(mtrDir2, HIGH);
      break;
  }
  analogWrite(mtrPwm1, max(0,speedFreq-offset));
  analogWrite(mtrPwm2, speedFreq);
}

void loop() {
    // when new data is written to bus then we want to run the motors, otherwise read from the ultrasonic sensors, refreshing every half second
  if(newData)
  {
    mtrCtrl(mtrCmd[1], mtrCmd[2]);
    newData = false;    //just read the new data
  }
}
