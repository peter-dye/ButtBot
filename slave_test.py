import smbus2
import time
from constants import SLAVE_ADDR

#Create the I2C bus
bus = smbus2.SMBus(1)

#Reads the distances from the slave
def writeI2C(address, speed, duration):
    pass



def main():
        speed = 1
        duration = 2
        address = SLAVE_ADDR
        print("Forward Test 2s")
        output=[speed*255, duration, 1]                     
        bus.write_i2c_block_data(address, register=0, data=output) 
        time.sleep(duration+0.2)
        print("backward test 2s")
        output=[speed*255, duration, 2]                     
        bus.write_i2c_block_data(address, register=0, data=output) 
        time.sleep(duration+0.2)
        print("left test 2s")
        output=[speed*255, duration, 3]                     
        bus.write_i2c_block_data(address, register=0, data=output) 
        time.sleep(duration+0.2)
        print("right test 2s")
        output=[speed*255, duration, 4]                     
        bus.write_i2c_block_data(address, register=0, data=output) 
        time.sleep(duration+0.2)
main()
