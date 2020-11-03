import Jetson.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD) #Set pin numbering type 

#Pin Declarations
PING_PIN1 = 11
ECHO_PIN1 = 13

'''
PING_PIN2 = 17
ECHO_PIN2 = 18

PING_PIN3 = 19
ECHO_PIN3 = 20

PING_PIN4 = 21
ECHO_PIN4 = 22
'''

#Distance Declarations
DANGER_DIST = 10
WARNING_DIST = 20

#Pin Type Setup
input_channels = [PING_PIN1]#, PING_PIN2, PING_PIN3, PING_PIN4]
output_channels = [ECHO_PIN1]#, ECHO_PIN2, ECHO_PIN3, ECHO_PIN4]
GPIO.setup(input_channels, GPIO.OUT, initial = GPIO.LOW) #Set all ping pins to outputs, default low 
GPIO.setup(output_channels, GPIO.IN, initial = GPIO.LOW) #Set all echo pins to inputs, default low

def microseconds_to_centimeters(duration):
    distance = duration / 29 / 2
    return distance

#Pulse trigger high for 10us, then measure time the echo pin is high, convert time to distance
def ping_ultrasonic_sensor(ping_pin, echo_pin):
    GPIO.output(ping_pin, GPIO.HIGH)                           #set ping high 
    time.sleep(0.000001)                                       #wait 10 microseconds
    GPIO.output(ping_pin, GPIO.LOW)                            #set ping low
    GPIO.wait_for_edge(echo_pin, GPIO.RISING)                  #wait for echo rising edge
    pulse_start = time.time()                                  #grab time echo goes high
    GPIO.wait_for_edge(echo_pin, GPIO.FALLING)                 #wait for echo falling edge
    pulse_end = time.time()                                    #grab time echo goes low
    duration = int((pulse_start - pulse_end) * 100000)         #echo pin is high for start - end microseconds
    distance = microseconds_to_centimeters(duration)           #convert duration to distance in centimeters
    return distance

while(true):
    #Acquire distances from each sensor
    d1 = ping_ultrasonic_sensor(PING_PIN1, ECHO_PIN1)
    #d2 = ping_ultrasonic_sensor(PING_PIN2, ECHO_PIN2)
    #d3 = ping_ultrasonic_sensor(PING_PIN3, ECHO_PIN3)
    #d4 = ping_ultrasonic_sensor(PING_PIN4, ECHO_PIN4)

    #If any sensors detect object in danger zone stop vehicle
    if(d1 < DANGER_DIST): #or d2 < DANGER_DIST or d3 < DANGER_DIST or d4 < DANGER_DIST):
        print("DANGER ZONE: VEHICLE STOPPED")
   #If any sensors detect object in warning zone slow vehicle
    elif(d1 < WARNING_DIST): # or d2 < WARNING_DIST or d3 < WARNING_DIST or d4 < WARNING_DIST):
        print("WARNING ZONE: VEHICLE SLOWING")
    #Print all senor readings
    print("Sensor 1 reads distance: ", d1)
    #print("Sensor 2 reads distance: ", d2)
    #print("Sensor 3 reads distance: ", d3)
    #print("Sensor 4 reads distance: ", d4)
