import board
import busio
import adafruit_pca9685
import smbus2 
bus = smbus2.SMBus(1)
pca = adafruit_pca9685.PCA9685(bus)

pca.frequency = 1600