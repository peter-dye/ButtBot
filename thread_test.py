import time 
from threading import Thread
from queue import Queue
import motor_driver
import smbus2        

bus = smbus2.SMBus(0)

q = Queue()
mc = motor_driver.MotorDriver(bus, q)
t1 = Thread(target = mc.consumer)
t1.start()

while True:
    info = input('Enter Speed and Time and Direction: ')
    input_dims = info.split()
    speed = float(input_dims[0])
    dur = float(input_dims[1])
    dir = str(input_dims[2])
    print("speed is", speed)
    print("duration is", dur)
    print("direction is", dir)
    mc.motor_send(speed, dur, dir)
    time.sleep(dur)

