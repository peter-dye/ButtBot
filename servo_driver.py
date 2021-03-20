from time import sleep
from adafruit_servokit import ServoKit
from constants import *

# Servo[5] controls the yaw of the camera. Mounted with 60 deg pointing straight forwards. 120 deg pans camera to the right
# until it is +180 degrees. 0 deg pans camera to the left until it is -180 degrees. 3:1 gear ratio mounted on servo 5
# Servo[6] controls the pitch of the camera. 

class ServoDriver():

    def __init__(self):
        self.kit = ServoKit(channels=8)
        self.pan = self.kit.servo[5]
        self.pitch = self.kit.servo[6]
        self.pan.actuation_range = 128

        self.default()

    #Return all servos to default position
    def default(self):
        self.pan.angle = 60
        self.pitch.angle = 90

    def pitch(self, pitch_angle):
        self.pitch.angle = pitch_angle

    def pan(self, target_ang):
        if target_ang > 0:
            while ((self.pan.angle-60)*3) < target_ang:
                self.pan.angle += 1
                time.sleep(0.300)
        
        elif target_ang < 0:
            while ((self.pan.angle-60)*3) > target_ang:
                self.pan.angle -= 1
                time.sleep(0.300)

    def read(self):
        return (round(self.pan.angle*3), round(self.pitch.angle))
     