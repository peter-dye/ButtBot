from time import sleep
from adafruit_servokit import ServoKit
from constants import *

# Servo[5] controls the yaw of the camera. Mounted with 60 deg pointing straight forwards. 120 deg pans camera to the right
# until it is +180 degrees. 0 deg pans camera to the left until it is -180 degrees. 3:1 gear ratio mounted on servo 5
# Servo[6] controls the pitch of the camera. 

class ServoDriver():

    def __init__(self):
        self.kit = ServoKit(channels=8)
        self.s_pan = self.kit.servo[5]
        self.s_pitch = self.kit.servo[6]
        self.s_pan.actuation_range = 128
        self.s_pitch.actuation_range = 126

        self.default()

    #Return all servos to default position
    def default(self):
        self.pan(0)
        self.pitch(90)

    def pitch(self, pitch_angle):
        self.s_pitch.angle = pitch_angle

    def pan(self, target_ang):
        if target_ang > (self.s_pan.angle-60)*3:
            while ((self.s_pan.angle-60)*3) < target_ang:
                if ((target_ang - (self.s_pan.angle-60)*3) < 3):
                    self.s_pan.angle += 1
                else:
                    self.s_pan.angle += 3
                sleep(0.400)
    
        elif target_ang < (self.s_pan.angle-60)*3:
            while ((self.s_pan.angle-60)*3) > target_ang:
                if ((((self.s_pan.angle-60)*3) - target_ang) < 3):
                    self.s_pan.angle = max(self.s_pan.angle-1, 0)
                else:
                    self.s_pan.angle = max(self.s_pan.angle-3, 0)
                sleep(0.400)

    def read(self):
        return (int((self.s_pan.angle-60)*3), round(self.s_pitch.angle))
     