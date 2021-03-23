from ultrasonic_driver import UltrasonicDriver
from motor_driver import MotorDriver
import time

md = MotorDriver()
ud = UltrasonicDriver()

while True:
    distances = ud.get_distances()
    if distances[0] < 20 or distances[1] < 20:
        md.stop()
    else:
        md.motor_send(1,100,'fwd')
    
    

