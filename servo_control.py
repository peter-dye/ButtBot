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

#function for scanning area for markers

#function to actuate arm for pickup routine
def actuate_arm():
    kit.servo[2].angle = 180    #lower arm
    time.delay(3)               #wait so has a chance to suck up butt
    kit.servo[2].angle = 0      #raise arm back to neutral position

