#!/usr/bin/env python3

from ultrasonic_driver import UltrasonicDriver
from motor_driver import MotorDriver
import time

md = MotorDriver()
ud = UltrasonicDriver()
time.sleep(10)
for i in range(5):
    print('sending', i)
    md.motor_send(1,100,'fwd')
    while md.running():
        distances = ud.get_distances()
        if distances[0] < 20 or distances[1] < 20:
            md.stop()
            while distances[0] < 20 or distances[1] < 20:
                distances = ud.get_distances()
            break
    time.sleep(1)
print("sleeping")
time.sleep(5)
md.stop()

    

