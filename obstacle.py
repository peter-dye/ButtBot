#!/usr/bin/env python3

from ultrasonic_driver import UltrasonicDriver
from motor_driver import MotorDriver
import time

md = MotorDriver()
ud = UltrasonicDriver()
#time.sleep(30)
for i in range(1):
    print('sending', i)
    md.motor_send(1,1000,'fwd')
 
print('stopping')
md.stop()

    

