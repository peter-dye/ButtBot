# NEED TO FIGURE OUT HOW BOT PHYSICALLY MOVES TO CHANGE PARAMETERS OF MOVEMENT FUNCTIONS
# WANT TO SPECIFY DISTANCE FOR FWD BWD, AND ANGLES FOR RIGHT AND LEFT

import time
from slave_test.py import bus
from constants import SLAVE_ADDR

class MotorDriver():

    def __init__(self):
        pass

    # Move both motors forwards at speed for duration
    def fwd_bwd(self, spd, dur, dir):
        if dir == 'fwd':
            coded_dir = 1
        elif dir == 'bwd':
            coded_dir = 2
        spd_in_freq = spd*255
        motor_command = [sped_in_freq, dur, coded_dir]
        bus.write_i2c_block_data(SLAVE_ADDR, register=0, data=motor_command) 
        time.sleep(dur+0.2)
        self.stop()

    # Move right motor backwards, while moving left motor forwards until desired angle
    def pivot_right_left(self, dur, dir):
        if dir == 'right':
            coded_dir = 4
        if dir == 'left':
            coded_dir = 3
        spd_in_freq = spd*255
        motor_command = [sped_in_freq, dur, coded_dir]
        bus.write_i2c_block_data(SLAVE_ADDR, register=0, data=motor_command) 
        time.sleep(dur+0.2)
        self.stop()

    # Stop both motors
    def stop(self):
        motor_command = [0,0.5,0]
        bus.write_i2c_block_data(SLAVE_ADDR, register=0, data=motor_command)

