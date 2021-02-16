import smbus2
import time
from constants import *

#Create the I2C bus
bus = smbus2.SMBus(1)

#Reads the distances from the slave
def writeI2C(address, speed, duration, direction):
    #speed = speed*255
    #bus.write_byte_data(address, 0, speed)                  
    #time.sleep(.100) 
    #bus.write_byte_data(address, 0, duration)
    #time.sleep(.100)    
    #if direction == 'fwd':
    #    dir = 0
    #elif direction == 'bwd':
    #    dir = 1
    #elif direction == 'left':
    #    dir = 2
    #elif direction == 'right':
    #    dir = 3
    #bus.write_byte_data(address, 0, dir)
    output=[3,2,4,7,1,3,5,6,9]                     
    bus.write_i2c_block_data(address, register=1, data=output) 


def main():
        writeI2C(SLAVE_ADDR, 0, 8, 'fwd')
        print("command sent")

main()
