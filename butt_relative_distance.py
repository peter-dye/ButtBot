import math
import servo_driver as sd
from path_planning import motor_controller

CAM_HEIGHT = 100        #Camera height off of ground in cm
CAM_OFFSET = 10         #Distance between straight below camera to center of collection arm nozzle in cm
IMG_HEIGHT = 2464          
IMG_WIDTH = 3280

def calc_distance(butt_x, butt_y):
    #butt is left of the bot
    if butt_x < IMG_WIDTH/2:
        if butt_y > IMG_HEIGHT/2:
            while (butt_y > IMG_HEIGHT/2):
                tilt_angle -= 1
                sd.camera_tilt(tilt_angle)
    
        else:
            while (butt_y < IMG_HEIGHT/2):
                tilt_angle += 1
                sd.camera_tilt(tilt_angle)

        x_dist = CAM_HEIGHT * math.tan(tilt_angle)

        pan_angle = sd.camera_pan(IMG_WIDTH, butt_x,'left')

        need_to_move = x_dist / math.cos(pan_angle)

        return need_to_move, pan_angle, 'left'

    #butt is right of the bot
    elif butt_x > IMG_WIDTH/2:
        if butt_y > IMG_HEIGHT/2:
            while (butt_y > IMG_HEIGHT/2):
                tilt_angle -= 1
                sd.camera_tilt(tilt_angle)
    
        else:
            while (butt_y < IMG_HEIGHT/2):
                tilt_angle += 1
                sd.camera_tilt(tilt_angle)

        x_dist = CAM_HEIGHT * math.tan(tilt_angle)

        pan_angle = sd.camera_pan(IMG_WIDTH, butt_x,'right')

        need_to_move = x_dist / math.cos(pan_angle)
        
        return need_to_move, pan_angle, 'left'