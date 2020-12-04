const int pingPin1 = 3; // Trigger Pin of Ultrasonic Sensor1
const int echoPin1 = 2; // Echo Pin of Ultrasonic Sensor1

const int pingPin2 = 4; // Trigger Pin of Ultrasonic Sensor2
const int echoPin2 = 5; // Echo Pin of Ultrasonic Sensor2

const int pingPin3 = 6; // Trigger Pin of Ultrasonic Sensor2
const int echoPin3 = 7; // Echo Pin of Ultrasonic Sensor2

const int pingPin4 = 8; // Trigger Pin of Ultrasonic Sensor2
const int echoPin4 = 9; // Echo Pin of Ultrasonic Sensor2

void setup() {
   Serial.begin(9600); // Starting Serial Terminal
}

void loop() {
   //Obtain sensor 1 info
   long duration1, cm1, duration2, cm2, duration3, cm3, duration4, cm4;
   pinMode(pingPin1, OUTPUT);
   pinMode(pingPin2, OUTPUT);
   pinMode(pingPin3, OUTPUT);
   pinMode(pingPin4, OUTPUT);
   pinMode(echoPin1, INPUT);
   pinMode(echoPin2, INPUT);
   pinMode(echoPin3, INPUT);
   pinMode(echoPin4, INPUT);
   digitalWrite(pingPin1, LOW);
   delayMicroseconds(2);
   digitalWrite(pingPin1, HIGH);
   delayMicroseconds(10);
   digitalWrite(pingPin1, LOW);
   duration1 = pulseIn(echoPin1, HIGH);
   cm1 = microsecondsToCentimeters(duration1);

   //Obtain sensor 2 info
   digitalWrite(pingPin2, LOW);
   delayMicroseconds(2);
   digitalWrite(pingPin2, HIGH);
   delayMicroseconds(10);
   digitalWrite(pingPin2, LOW);
   duration2 = pulseIn(echoPin2, HIGH);
   cm2 = microsecondsToCentimeters(duration2);

   //Obtain sensor 3 info
   digitalWrite(pingPin3, LOW);
   delayMicroseconds(2);
   digitalWrite(pingPin3, HIGH);
   delayMicroseconds(10);
   digitalWrite(pingPin3, LOW);
   duration3 = pulseIn(echoPin3, HIGH);
   cm3 = microsecondsToCentimeters(duration3);

   //Obtain sensor 4 info
   digitalWrite(pingPin4, LOW);
   delayMicroseconds(2);
   digitalWrite(pingPin4, HIGH);
   delayMicroseconds(10);
   digitalWrite(pingPin4, LOW);
   duration4 = pulseIn(echoPin4, HIGH);
   cm4 = microsecondsToCentimeters(duration4);
   
   if(cm1 < 10 || cm2 < 10 || cm3 < 10 || cm4 < 10){
    Serial.print("DANGER ZONE: VEHICLE STOPPED");
    Serial.println();
    delay(500);
   }

   else if((cm1 > 10 || cm2 > 10 || cm3 > 10 || cm4 > 10) && (cm1 < 20 || cm2 < 20 || cm3 > 10 || cm4 > 10)){
    Serial.print("WARNING ZONE: VEHICLE SLOWING");
    Serial.println();
    delay(500);
   }

   else{
   //Print Sensor 1 info
   Serial.print("Sensor 1: ");
   Serial.print(cm1);
   Serial.print("cm");
   Serial.println();
   
  //Print Sensor 2 info
   Serial.print("Sensor 2: ");
   Serial.print(cm2);
   Serial.print("cm");
   Serial.println();
   delay(100);

   //Print Sensor 1 info
   Serial.print("Sensor 3: ");
   Serial.print(cm3);
   Serial.print("cm");
   Serial.println();

   //Print Sensor 1 info
   Serial.print("Sensor 4: ");
   Serial.print(cm4);
   Serial.print("cm");
   Serial.println();
  }

}

long microsecondsToCentimeters(long microseconds) {
   return microseconds / 29 / 2;
}
