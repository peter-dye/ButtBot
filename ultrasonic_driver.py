import smbus2
import time
#import motor_driver
#from path_planning import motor_controller

#Address of slave, must match address in slave sketch
SLAVE_ADDR = 9

#List of distances read by each sensor
distance = []

#Create the I2C bus
bus = smbus2.SMBus(1)

#Reads the distances from the slave
def readI2C(address):
    bval = 0                                #Temp variable to store the byte read from the bus
    time.sleep(.100)                        #Pause for 100ms
    bval = bus.read_byte_data(address, 0)   #Read the byte from the bus
    return bval                             #Return read byte

def main():
    while True:
        while(readI2C(SLAVE_ADDR) < 255):              #255 is the start byte, so if we read in the middle of a transmission, wait until next start
            for bcount in range(4):
                distance[bcount] = readI2C(SLAVE_ADDR) #Put each distance in the list in its respective position
                print(bcount, distance[bcount])
                # if(distance[bcount] < 100):
                #     motor_controller.stop()
                #     time.sleep(1)
            time.sleep(.200)                           #Delay for 200ms

main()
