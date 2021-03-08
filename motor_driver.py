# NEED TO FIGURE OUT HOW BOT PHYSICALLY MOVES TO CHANGE PARAMETERS OF MOVEMENT FUNCTIONS
# WANT TO SPECIFY DISTANCE FOR FWD BWD, AND ANGLES FOR RIGHT AND LEFT
import math
import time
from constants import SLAVE_ADDR

class MotorDriver():

    def __init__(self, bus, queue):
        self.bus = bus
        self.q = queue

    # Move both motors forwards at speed for duration
    def fwd_bwd(self, spd, dir):
        if dir == 'fwd':
            coded_dir = 1
        elif dir == 'bwd':
            coded_dir = 2
        spd_in_freq = int(spd*255)
        motor_command = [spd_in_freq, coded_dir]
        self.bus.write_i2c_block_data(SLAVE_ADDR, register=0, data=motor_command) 

    # Move right motor backwards, while moving left motor forwards until desired angle
    def pivot(self, speed, dir):
        if dir == 'left':
            coded_dir = 3
        if dir == 'right':
            coded_dir = 4
        spd_in_freq = 255
        motor_command = [spd_in_freq, coded_dir]
        self.bus.write_i2c_block_data(SLAVE_ADDR, register=0, data=motor_command) 

    # Stop both motors
    def stop(self):
        motor_command = [0,0]
        self.bus.write_i2c_block_data(SLAVE_ADDR, register=0, data=motor_command)

    def motor_send(self, speed, duration, direction):
        data = [0,0,0]
        data[0] = speed
        data[1] = duration 
        data[2] = direction 
        self.q.put(data)

    def consumer(self):
        while True:
            data = self.q.get()
            if data[2] == 'fwd' or data[2] == 'bwd':
                self.fwd_bwd(data[0], data[2])
            elif data[2] == 'right' or data[2] == 'left':
                self.pivot(data[0],data[2])
            else:
                print("not a valid direction")
                self.stop()
                while True:
                    pass
            global running
            running = True
            time.sleep(data[1])
            mc.stop()

