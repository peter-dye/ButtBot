import smbus2
import time
from constants import *
#import motor_driver
#from path_planning import motor_controller


#List of distances read by each sensor
distance = [0, 0, 0, 0, 0]

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
        while(readI2C(SLAVE_ADDR) < 255): #255 is the start byte, so if we read in the middle of a transmission, wait until next start
            print("Waiting")               #new             
        for bcount in range(5):
            distance[bcount] = readI2C(SLAVE_ADDR) #Put each distance in the list in its respective position
            if(distance[bcount] < 100):
                motor_controller.stop()
                time.sleep(1)
        print("0: "+str(distance[0])+
                " 1: "+str(distance[1])+
                " 2: "+str(distance[2])+
                " 3: "+str(distance[3])+
                " 4: "+str(distance[4]))
        time.sleep(.200)                           #Delay for 200ms

main()
