#import time 
#from threading import Thread
#from queue import Queue
#import motor_driver
#import smbus2        

#bus = smbus2.SMBus(0)

#q = Queue()
#mc = motor_driver.MotorDriver(q)
#t1 = Thread(target = mc.consumer)
#t1.start()

#while True:
#    info = input('Enter Speed and Time and Direction: ')
#    input_dims = info.split()
#    speed = float(input_dims[0])
#    dur = float(input_dims[1])
#    dir = str(input_dims[2])
#    print("speed is", speed)
#    print("duration is", dur)
#    print("direction is", dir)
#    mc.motor_send(speed, dur, dir)
#    time.sleep(dur)

#import random as r

#for i in range(10):
#    print(r.randint(1,3))
baba = False
for i in range(10):
    if baba:
        break
    if i == 6: 
        print("breaking")
        break
    if i == 3:
        baba = True
    print(i)