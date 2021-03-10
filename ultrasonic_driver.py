import time
from constants import *
#import motor_driver
#from path_planning import motor_controller

class UltrasonicDriver():

    def __init__(self, bus, buffer, lock):
        self.bus = bus
        self.buffer = buffer
        self.lock = lock
    #Reads the distances from the slave
    def readI2C(self):
        bval = 0                                        #Temp variable to store the byte read from the bus
        bval = self.bus.read_byte_data(SLAVE_ADDR, 0)   #Read the byte from the bus
        return bval                                     #Return read byte

    def write_to_mem(self):
        while True:
            self.lock.acquire()
            while (self.readI2C() < 255):
                        pass
            for i in range(4):
                self.buffer[i] = self.readI2C()
            self.lock.release()
            time.sleep(0.200)

    def read_from_mem(self):
            temp = [0,0,0,0]
            self.lock.acquire()
            for i in range(4):
                temp[i] = self.buffer[i]
            self.lock.release()
            return temp




