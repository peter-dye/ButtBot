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
        if data[2] == 'fwd' or data[2] == 'bwd':
            mc.fwd_bwd(data[0], data[2])
        elif data[2] == 'right' or data[2] == 'left':
            mc.pivot(data[0],data[2])
        else:
            print("not a valid direction")
            while True:
                pass
        time.sleep(data[1])
        print("leaving")
        mc.stop()
        

bus = smbus2.SMBus(0)
mc = motor_driver.MotorDriver(bus)

q = Queue()
t1 = Thread(target = consumer, args = (q, ))
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
    motor_send(speed, dur, dir)
    time.sleep(dur)

