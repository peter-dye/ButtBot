import time
from adafruit_servokit import ServoKit

## Servo[3] is for controlling collection arm. Mounted with 0 deg meaning arm is fully in up position
## Servo[2] controls the pitch of the camera. Mounted with 0 deg has camera pointing straight downwards
## Servo[1] and Servo[0] control the yaw of the camera. Servo[1] is mounted onto Servo[0].  
## Mounted with 90 deg on both [1] and [0] at 90 deg means camera pointing straight forward

kit = ServoKit(channels=16)

def startup():
    #Initial sweep Servo[0]
    kit.servo[0].angle =  180
    kit.servo[0].angle = 0
    #Initial sweep Servo[1]
    kit.servo[1].angle =  180
    kit.servo[1].angle = 0
    #Initial sweep Servo[2]
    kit.servo[2].angle = 180
    kit.servo[2].angle = 0
    #Initial sweep Servo[3]
    kit.servo[3].angle = 180
    kit.servo[3].angle = 0
    default()

#Return all servos to default position
def default():
    kit.servo[0].angle =  90
    kit.servo[1].angle = 90
    kit.servo[2].angle = 30
    kit.servo[3].angle = 0 

#Actuate arm for pickup routine
def actuate_arm():
    kit.servo[3].angle = 180    #lower arm
    time.delay(3)               #wait 3 seconds while lowered so has a chance to suck up butt
    kit.servo[3].angle = 0      #raise arm back to neutral position

def servo_read(direction):
    if direction == 'RIGHT':    #to sweep right the servos will only be moving from 90 to 180 degrees
        min_angle = 90
        max_angle = 180
        inc = 1
    elif direction == 'LEFT':   #to sweep left the servos will only be moving from 90 to 0 degrees
        min_angle = 0
        max_angle = 90 
        inc = -1
    angle1 = sweep(min_angle, max_angle, inc, 0) - 90        #Subtracts 90 to get the position w.r.t. the 90 degrees start point
    if angle1 == -90 or angle1 == 90:                        #If the first servo hasn't detected the marker in its max range
        angle2 = sweep(min_angle, max_angle, inc, 1) - 90    #Move the second servo
    else:
        angle2 = 0  
    angle_detected = angle1 + angle2                         #The marker is detected at the sum of both angles

def sweep(min_angle, max_angle, inc, servo_num):
    angle = 90                                          #Servo always starting at default 90 deg
    for angle in range(min_angle, max_angle):           #Move servo degree by degree
        kit.servo[servo_num].angle = angle              
        #if(markerdetected):                             #If marker is detected return current servo angle
            #return angle
        #else:
            #angle += inc                                  #Keep moving servo
        angle += inc
