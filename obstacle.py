#!/usr/bin/env python3

from ultrasonic_driver import UltrasonicDriver
from motor_driver import MotorDriver
import time

md = MotorDriver()
ud = UltrasonicDriver()

for i in range(5):
    md.motor_send(1,100,'fwd')
    while True:
        distances = ud.get_distances()
        print(distances)
        if distances[0] < 20 or distances[1] < 20:
            md.stop()
            while distances[0] < 20 or distances[1] < 20:
                distances = ud.get_distances()
                print(distances)
            break

    

