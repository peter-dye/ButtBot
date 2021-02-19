import smbus2
import time
from constants import *
#import motor_driver
#from path_planning import motor_controller

class UltrasonicDriver():

    def __init__(self, bus):
        #List of distances read by each sensor
        self.distance = [0, 0, 0, 0, 0]
        self.bus = bus

    #Reads the distances from the slave
    def readI2C(address):
        bval = 0                                #Temp variable to store the byte read from the bus
        time.sleep(.100)                        #Pause for 100ms
        bval = bus.read_byte_data(address, 0)   #Read the byte from the bus
        return bval                             #Return read byte




