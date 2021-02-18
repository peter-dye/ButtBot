# NEED TO FIGURE OUT HOW BOT PHYSICALLY MOVES TO CHANGE PARAMETERS OF MOVEMENT FUNCTIONS
# WANT TO SPECIFY DISTANCE FOR FWD BWD, AND ANGLES FOR RIGHT AND LEFT

import time
from constants import SLAVE_ADDR

class MotorDriver():

    def __init__(self,bus):
        self.bus = bus

    # Move both motors forwards at speed for duration
    def fwd_bwd(self, spd, dur, dir):
        if dir == 'fwd':
            coded_dir = 1
        elif dir == 'bwd':
            coded_dir = 2
        spd_in_freq = spd*255
        motor_command = [sped_in_freq, dur, coded_dir]
        self.bus.write_i2c_block_data(SLAVE_ADDR, register=0, data=motor_command) 
        time.sleep(dur+0.2)
        self.stop()

    # Move right motor backwards, while moving left motor forwards until desired angle
    def pivot(self, dur, dir):
        if dir == 'left':
            coded_dir = 3
        if dir == 'right':
            coded_dir = 4
        spd_in_freq = 255
        motor_command = [sped_in_freq, dur, coded_dir]
        self.bus.write_i2c_block_data(SLAVE_ADDR, register=0, data=motor_command) 
        time.sleep(dur+0.2)
        self.stop()

    # Stop both motors
    def stop(self):
        motor_command = [0,0.5,0]
        self.bus.write_i2c_block_data(SLAVE_ADDR, register=0, data=motor_command)

