import time
from smbus2 import SMBus
from constants import *
from multiprocessing import Array
from threading import Thread, Lock
#import motor_driver
#from path_planning import motor_controller


class UltrasonicDriver():

    def __init__(self):
        self.bus = SMBus(0)
        self.buffer = Array('I', range(4))
        self.lock = Lock()

        self.t = Thread(target=self.write_to_mem)
        self.t.start()

    def readI2C(self):
        #Reads the distances from the slave
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

    def get_distances(self):
        return self.read_from_mem()
