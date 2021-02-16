import smbus2
import time
from constants import *

#Create the I2C bus
bus = smbus2.SMBus(1)

#Reads the distances from the slave
def writeI2C(address, speed, duration, direction):
    bus.write_byte_data(address, 0, speed)                  
    time.sleep(.100) 
    bus.write_byte_data(address, 0, duration)
    time.sleep(.100)    
    if direction == 'fwd':
        dir = 0
    elif direction == 'bwd':
        dir = 1
    elif direction == 'left':
        dir = 2
    elif direction == 'right':
        dir = 3
    bus.write_byte_data(address, 0, dir)                              

def main():
    i = 0
    for j in range(3):
        speed = i % 3
        writeI2C(SLAVE_ADDR, speed, 1, 'fwd')
        print("command sent")

main()
