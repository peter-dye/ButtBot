import math
import servo_driver as sd
from path_planning import motor_controller
from constants import *

class RelativeButt():

    def __init__(self, servo_driver, butt_coords):
        self.servo_driver = servo_driver
        self.butt_x = butt_coords[0]
        self.butt_y = butt_coords[1]
        self.need_to_move = 0
        self.pan_angle = 0 

        calc_distance()

        return(self.need_to_move, self.pan_angle)

    def calc_distance(self):
        #butt is left of the bot
        current_angles = self.servo_driver.read()
        target_pan = current_angles[0]
        tilt_angle = current_angles[1]

        if self.butt_x < IMG_WD/2:
            if self.butt_y > IMG_HT/2:
                while (self.butt_y > IMG_HT/2):
                    tilt_angle -= 1
                    self.servo_driver.pitch(tilt_angle)
                    
            else:
                while (self.butt_y < IMG_HT/2):
                    tilt_angle += 1
                    self.servo_driver.pitch(tilt_angle)

            x_dist = CAM_HEIGHT * math.tan(tilt_angle)

            while (self.butt_x < IMG_WD/2):
                target_pan -= 1
                self.servo_driver.pan(target_pan)
                self.pan_angle = target_pan

            self.need_to_move = x_dist / math.cos(self.pan_angle)

        #butt is right of the bot
        elif self.butt_x > IMG_WD/2:
            if self.butt_y > IMG_HT/2:
                while (self.butt_y > IMG_HT/2):
                    tilt_angle -= 1
                    self.servo_driver.pitch(tilt_angle)
    
            else:
                while (self.butt_y < IMG_HT/2):
                    tilt_angle += 1
                    self.servo_driver.pitch(tilt_angle)

            x_dist = CAM_HEIGHT * math.tan(tilt_angle)

            while (self.butt_x > IMG_WD/2):
                target_pan += 1
                self.servo_driver.pan(target_pan)
                self.pan_angle = target_pan

            self.need_to_move = x_dist / math.cos(self.pan_angle)
        