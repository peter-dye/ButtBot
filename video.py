from motor_driver import MotorDriver
from arm_driver import ArmDriver
import time


def run():
    md = MotorDriver()

    while True:
        time.sleep(10)
        md.motor_send(1, 10, 'fwd')
        time.sleep(10)

def arun():
    arm = ArmDriver()
    arm.pickup()
    time.sleep(10)
    
