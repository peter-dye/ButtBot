import board
import busio
import time
import adafruit_pca9685


i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)

pca.frequency = 60

mtr1_channel = pca.channels[8]

mtr1_channel.duty_cycle = 0xFFFF
time.sleep(1)
mtr1_channel.duty_cycle = 0x0000
time.sleep(1)

pca.channels[7].duty_cycle = 0x0000
time.sleep(1)
pca.channels[7].duty_cycle = 0xFFFF