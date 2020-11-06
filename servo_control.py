import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

#Initial sweep servo 1
kit.servo[0].angle =  180
kit.servo[0].angle = 0

#Initial sweep servo 2
kit.servo[1].angle =  180
kit.servo[1].angle = 0

#Initial sweep servo 3
kit.servo[2].angle = 180
kit.servo[2].angle = 0

#Initial sweep servo 4
kit.servo[3].angle = 180
kit.servo[3].angle = 0

#function for scanning area for markers

#function to actuate arm for pickup routine
def actuate_arm():
    kit.servo[3].angle = 180    #lower arm
    time.delay(3)               #wait 3 seconds while lowered so has a chance to suck up butt
    kit.servo[3].angle = 0      #raise arm back to neutral position

def sweep_camera():
    kit.servo[2].angle = 90     #lift camera to be pointing straight outwards
    kit.servo[0].angle = 180
    kit.servo[1].angle = 180    #move camera in a full 30 degrees
    default()

def default():
    kit.servo[2].angle = 0
    kit.servo[0].angle = 0
    kit.servo[1].angle = 0