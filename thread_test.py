import time 
from threading import Thread
from queue import Queue
import motor_driver
import smbus2

def motor_send(out_q, speed, duration, direction):
    data = [0,0,0]
    data[0] = speed
    data[1] = duration 
    data[2] = direction 
    out_q.put(data)

def consumer(in_q):
    while True:
        data = in_q.get()
        print("in here")
        mc.fwd_bwd(data[0], data[2])
        time.sleep(data[1])
        print("leaving")
        mc.stop()
        

bus = smbus2.SMBus(0)
mc = motor_driver.MotorDriver(bus)

q = Queue()
t1 = Thread(target = consumer, args = (q, ))
t1.start()


motor_send(q, 1, 1.6, 'fwd')

t1.join()