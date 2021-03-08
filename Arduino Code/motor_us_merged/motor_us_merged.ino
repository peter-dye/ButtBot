// Import wire library to be able to use i2c communicaiton
#include <Wire.h>

// Import library to use ultrasonic sensors
#include <NewPing.h>

// Define slave address
#define SLAVE_ADDR 9

// Define the motor control pins
#define mtrPwm1 9
#define mtrDir1 11
#define mtrPwm2 10
#define mtrDir2 12

// HC-SR04 sensors are hooked up in 1-pin mode
#define PING_PIN_0 3 // Trigger Pin of Ultrasonic Sensor 0
#define ECHO_PIN_0 3 // Echo Pin of Ultrasonic Sensor 0

#define PING_PIN_1 4 // Trigger Pin of Ultrasonic Sensor 1
#define ECHO_PIN_1 4 // Echo Pin of Ultrasonic Sensor 1

#define PING_PIN_2 5 // Trigger Pin of Ultrasonic Sensor 2
#define ECHO_PIN_2 5 // Echo Pin of Ultrasonic Sensor 2

#define PING_PIN_3 6 // Trigger Pin of Ultrasonic Sensor 3
#define ECHO_PIN_3 6 // Echo Pin of Ultrasonic Sensor 3

// Define the maximum distance for the sensors to register: 260cm
#define MAX_DISTANCE 260

// Create ultrasonic sensor objects
NewPing sensor0(PING_PIN_0, ECHO_PIN_0, MAX_DISTANCE);
NewPing sensor1(PING_PIN_1, ECHO_PIN_1, MAX_DISTANCE);
NewPing sensor2(PING_PIN_2, ECHO_PIN_2, MAX_DISTANCE);
NewPing sensor3(PING_PIN_3, ECHO_PIN_3, MAX_DISTANCE);

// Initialize ultrasonic sensor return data array, one element per sensor
int distance[4];

// Initialize counter to count bytes in ultrasonic sensor response
int bcount = 0;

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

  // Tell slave which function to run upon master request (ultrasonic sensor information)
  Wire.onRequest(requestEvent);
  
  // To be able to look at serial monitor when running code for test
  Serial.begin(9600);
}

void requestEvent() {

  // Define a byte to hold data
  byte bval;

  // Cycle through data
  // First response is always 255 to mark beginning
  switch (bcount) {
    case 0:
      bval = 255;
      break;
    case 1:
      bval = distance[0];
      break;
    case 2:
      bval = distance[1];
      break;
    case 3:
      bval = distance[2];
      break;
    case 4:
      bval = distance[3];
      break;
  }

  // Send response back to Master
  Wire.write(bval);

  // Increment byte counter
  bcount = bcount + 1;
  if (bcount > 4) bcount = 0;

}

void receiveEvent(int howMany) {
  while (Wire.available()) { // loop through all but the last
    for(int i = 0; i < 3; i++){
      mtrCmd[i] = Wire.read();
    }
  }
  newData = true;
}

void readDistance()
{
  //Get the distance from each sensor, if object further than 255cm, clamp to 254 so as not to confuse I2C transmission into thinking start bit being transmitted
  distance[0] = sensor0.ping_cm();
  if (distance[0] > 254 ) {
    distance[0] = 254;
  }
  delay(20);

  distance[1] = sensor1.ping_cm();
  if (distance[1] > 254 ) {
    distance[1] = 254;
  }
  delay(20);

  distance[2] = sensor2.ping_cm();
  if (distance[2] > 254 ) {
    distance[2] = 254;
  }
  delay(20);

  distance[3] = sensor3.ping_cm();
  if (distance[3] > 254 ) {
    distance[3] = 254;
  }
  delay(20);
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
  analogWrite(mtrPwm2, max(0,speedFreq));
}

void loop() {
    // when new data is written to bus then we want to run the motors, otherwise read from the ultrasonic sensors, refreshing every half second
  if(newData)
  {
    mtrCtrl(mtrCmd[1], mtrCmd[2]);
    newData = false;    //just read the new data
  }
  readDistance();
}
