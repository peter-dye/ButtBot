import time 
from threading import Thread
from queue import Queue
import motor_driver
import ultrasonic_driver
import smbus2       

bus = smbus2.SMBus(0)
mc = motor_driver.MotorDriver(bus)
ud = ultrasonic_driver.UltrasonicDriver(bus) 

motor_q = Queue()
t1 = Thread(target = consumer, args = (motor_q, ))
t1.start()
distance = [0,0,0,0]

while True:
    running = False
    info = input('Enter Speed and Time and Direction: ')
    input_dims = info.split()
    speed = float(input_dims[0])
    dur = float(input_dims[1])
    dir = str(input_dims[2])
    print("speed is", speed)
    print("duration is", dur)
    print("direction is", dir)
    motor_send(motor_q, speed, dur, dir)
    while running == True:
        while (ud.readI2C() < 255):
            pass
        for i in range(1):
            distance[i] = ud.readI2C()
            if distance[i] < 30:
                mc.stop()
                print("stopped")
            print("Distance ", i , 'is ', distance[i])
