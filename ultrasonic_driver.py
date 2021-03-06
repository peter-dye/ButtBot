import smbus2
import time
from constants import *
#import motor_driver
#from path_planning import motor_controller

class UltrasonicDriver():

    def __init__(self, bus):
        self.bus = bus

    #Reads the distances from the slave
    def readI2C(self):
        bval = 0                                        #Temp variable to store the byte read from the bus
        bval = self.bus.read_byte_data(SLAVE_ADDR, 0)   #Read the byte from the bus
        return bval                                     #Return read byte




