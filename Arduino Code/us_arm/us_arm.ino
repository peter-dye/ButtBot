// Import wire library to be able to use i2c communicaiton
#include <Wire.h>

// Import library to use ultrasonic sensors
#include <NewPing.h>

// Import library to control servo
#include <Servo.h>

// Create Servo object
Servo armServo;

// Define slave address
#define SLAVE_ADDR 9

// HC-SR04 sensors are hooked up in 1-pin mode
#define PING_PIN_0 3 // Trigger Pin of Ultrasonic Sensor 0
#define ECHO_PIN_0 3 // Echo Pin of Ultrasonic Sensor 0

#define PING_PIN_1 4 // Trigger Pin of Ultrasonic Sensor 1
#define ECHO_PIN_1 4 // Echo Pin of Ultrasonic Sensor 1

#define PING_PIN_2 5 // Trigger Pin of Ultrasonic Sensor 2
#define ECHO_PIN_2 5 // Echo Pin of Ultrasonic Sensor 2

#define PING_PIN_3 6 // Trigger Pin of Ultrasonic Sensor 3
#define ECHO_PIN_3 6 // Echo Pin of Ultrasonic Sensor 3

// Define Fan Enable input and output
#define FAN_IN 9
#define FAN_OUT 2

// Define Arm input and output
#define ARM_IN 10
#define ARM_OUT 8


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

void setup() {
  // Initialize fan enable I/O
  pinMode(FAN_IN, INPUT);
  pinMode(FAN_OUT, OUTPUT);

  // Initialize arm control pin
  pinMode(ARM_IN, INPUT);

  // Tell servo which pin controls it and initialize to down position of servo at 7 deg
  armServo.attach(ARM_OUT);
  armServo.write(7);
  
  // Initialize I2C communications as slave
  Wire.begin(SLAVE_ADDR);

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

void loop() {
  // If Jetson Nano sets fan_in to high, turn on fan with fan_out = low. Default is fan off with fan_out == high
  if (digitalRead(FAN_IN)){
    digitalWrite(FAN_OUT, LOW);
  }
  else{
    digitalWrite(FAN_OUT, HIGH);
  }

  // If jetson nano sets arm_in to high, rais arm by setting servo to 170 deg. Default is arm down with servo at 7 deg.
  if (digitalRead(ARM_IN)){
    armServo.write(170);
  }
  else{
    armServo.write(7);
  }

  // Read distances from ultrasonic sensor array, refreshing every 200ms
  readDistance();
  delay(200);
}
