from multiprocessing import Process, Array
import time 
from threading import Thread, Lock
from queue import Queue
import motor_driver
import ultrasonic_driver
import smbus2      
import path_Q

# Create i2c busses
ard_bus = smbus2.SMBus(0)

# Create motor q, thread, and motor controller
motor_q = Queue()
motor_thread = Thread(args = (motor_q, ))
motor_thread.start()
mc = motor_driver.MotorDriver(ard_bus, motor_q)

# Create US shared memory, shared mem buffer, lock, US thread, and ultrasonic sensor driver
us_buffer = Array('I', range(4))
shm_a = Process()
shm_a.start()
us_lock = Lock()
us = ultrasonic_driver.UltrasonicDriver(ard_bus, us_buffer, us_lock) 
us_thread = Thread(target = us.write_to_mem)
us_thread.start()

path_q = Queue()
path_thread = Thread(target = path_Q.put_cmd, args=(path_q))
path_thread.start()

while True:
    mtr_cmd = path_q.get()
    mc.motor_send(mtr_cmd[0], mtr_cmd[1], mtr_cmd[2])

    distance = us.read_from_mem()
    for i in range(len(distance)):
        if distance[i] < 30:
            mc.stop()
