import math
import servo_driver
import motor_driver
from path_planning import motor_controller

CAM_HEIGHT = 100        #Camera height off of ground in cm
CAM_OFFSET = 10         #Distance between straight below camera to center of collection arm nozzle in cm
IMG_HEIGHT = 0          
IMG_WIDTH = 0

#butt is left of the bot
if butt_x < IMG_WIDTH/2:
    if butt_y > IMG_HEIGHT/2:
        while (butt_y > IMG_HEIGHT/2):
            tilt_angle += 1
    
    else:
        while (butt_y < IMG_HEIGHT/2):
            tilt_angle -= 1

    x_dist = CAM_HEIGHT * math.tan(tilt_angle)

    while (butt_x < IMG_WIDTH/2): 
        pan_angle -= 1

    need_to_move = x_dist / math.cos(pan_angle)

    motor_controller.pivot_right_left(pan_angle, 'left')
    motor_controller.fwd_bwd(speed,need_to_move,'fwd')

#butt is right of the bot
if butt_x > IMG_WIDTH/2:
    if butt_y > IMG_HEIGHT/2:
        while (butt_y > IMG_HEIGHT/2):
            tilt_angle += 1
    
    else:
        while (butt_y < IMG_HEIGHT/2):
            tilt_angle -= 1

    x_dist = CAM_HEIGHT * math.tan(tilt_angle)

    while (butt_x > IMG_WIDTH/2): 
        pan_angle += 1

    need_to_move = x_dist / math.cos(pan_angle)

    motor_controller.pivot_right_left(pan_angle, 'right')
    motor_controller.fwd_bwd(speed,need_to_move,'fwd')