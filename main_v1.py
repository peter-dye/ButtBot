from multiprocessing import Process, Array
import time 
from threading import Thread, Lock
from queue import Queue
import motor_driver
import ultrasonic_driver
import smbus2      
import path_Q
import arm_driver
import Jetson.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Create i2c busses
ard_bus = smbus2.SMBus(0)

# Create motor q, thread, and motor controller
motor_q = Queue()
mc = motor_driver.MotorDriver(motor_q)
motor_thread = Thread(target = mc.motor_consume)
motor_thread.start()

# Create US shared memory, shared mem buffer, lock, US thread, and ultrasonic sensor driver
us_buffer = Array('I', range(4))
shm_a = Process()
shm_a.start()
us_lock = Lock()
us = ultrasonic_driver.UltrasonicDriver(ard_bus, us_buffer, us_lock) 
us_thread = Thread(target = us.write_to_mem)
us_thread.start()

path_q = Queue()
path_thread = Thread(target = path_Q.put_cmd, args=(path_q,))
path_thread.start()
mtr_cmd = [0,0,0,0]

arm_q = Queue()
arm = arm_driver.Arm(arm_q)
arm_thread = Thread(target = arm.arm_consume)
arm_thread.start

count = 0
while True:
    if not path_q.empty():
        mtr_cmd = path_q.get() 
        mc.motor_send(mtr_cmd[0], mtr_cmd[1], mtr_cmd[2])
        arm.arm_send(mtr_cmd[3])

    distance = us.read_from_mem()
    for i in range(1):
        if distance[i] < 10:
            print("stop!")
            mc.stop()
    if count % 100 == 0:
        print("US dist: ", distance[i])
    count += 1

