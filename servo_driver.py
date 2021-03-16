from time import sleep
from adafruit_servokit import ServoKit
from constants import *

## Servo[4] is for controlling collection arm. Mounted with 0 deg meaning arm is fully in down position
## Servo[5] controls the pitch of the camera. Mounted with 0 deg has camera pointing straight downwards
## Servo[6] and Servo[7] control the yaw of the camera.
## Mounted with 90 deg on both [6] and [7] at 90 deg means camera pointing straight forward

class ServoDriver():

    def __init__(self):
        self.kit = ServoKit(channels=8)
        self.default()

    #Return all servos to default position
    def default(self):
        self.kit.servo[6].angle = 90
        self.kit.servo[7].angle = 90
        sleep(0.45)
        self.kit.servo[5].angle = 30
        sleep(0.45)
        print(self.kit.servo[5].angle)

    def tilt(self, pitch_angle):
        self.kit.servo[5].angle = pitch_angle

    def pan(self, pan_angle):
        if pan_angle > 90:
            self.kit.servo[6].angle = 180
            self.kit.servo[7].angle = 90 + (pan_angle - 90)
        elif pan_angle > 0:
            self.kit.servo[6].angle = 90 + pan_angle
        elif pan_angle < -90:
            self.kit.servo[6].angle = 0
            self.kit.servo[7].angle = 90 - (pan_angle + 90)
        else:
            self.kit.servo[6].angle = 90 - pan_angle
            
servo = ServoDriver()