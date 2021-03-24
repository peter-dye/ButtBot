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
    while md.running():
        distances = ud.get_distances()
        print(distances[0],distances[1])
        if distances[0] < 30 or distances[1] < 30:
            md.stop()
            while distances[0] < 30 or distances[1] < 30:
                distances = ud.get_distances()
                print(distances[0],distances[1])
            break
    time.sleep(1)
print("sleeping")
time.sleep(5)
md.stop()

    

