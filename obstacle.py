#!/usr/bin/env python3

from ultrasonic_driver import UltrasonicDriver
from motor_driver import MotorDriver
import time

md = MotorDriver()
ud = UltrasonicDriver()
#time.sleep(30)
for i in range(5):
    print('sending', i)
    md.motor_send(1,100,'fwd')

time.sleep(10)
print('stopping')
md.stop()

    

