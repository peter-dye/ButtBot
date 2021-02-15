import math
import servo_driver as sd
from path_planning import motor_controller
from constants import *

def calc_distance(butt_x, butt_y):
    #butt is left of the bot
    if butt_x < IMG_WD/2:
        if butt_y > IMG_HT/2:
            while (butt_y > IMG_HT/2):
                tilt_angle -= 1
                sd.camera_tilt(tilt_angle)
    
        else:
            while (butt_y < IMG_HT/2):
                tilt_angle += 1
                sd.camera_tilt(tilt_angle)

        x_dist = CAM_HEIGHT * math.tan(tilt_angle)

        pan_angle = sd.camera_pan(IMG_WD, butt_x,'left')

        need_to_move = x_dist / math.cos(pan_angle)

        return need_to_move, pan_angle, 'left'

    #butt is right of the bot
    elif butt_x > IMG_WD/2:
        if butt_y > IMG_HT/2:
            while (butt_y > IMG_HT/2):
                tilt_angle -= 1
                sd.camera_tilt(tilt_angle)
    
        else:
            while (butt_y < IMG_HT/2):
                tilt_angle += 1
                sd.camera_tilt(tilt_angle)

        x_dist = CAM_HEIGHT * math.tan(tilt_angle)

        pan_angle = sd.camera_pan(IMG_WD, butt_x,'right')

        need_to_move = x_dist / math.cos(pan_angle)
        
        return need_to_move, pan_angle, 'left'