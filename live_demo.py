from motor_driver import MotorDriver
from servo_driver import ServoDriver
from arm_driver import ArmDriver

md = MotorDriver()
sd = ServoDriver()
ad = ArmDriver()

def drive():
    for i in range(3):
        md.motor_send(1, 75, 'fwd')

def turn():
    for i in range(2):
        md.motor_send(1, 90, 'right')

def pickup():
    ad.pickup()

def up():
    ad.up()

def down():
    ad.down()

def pan(angle):
    sd.pan(angle)

def pitch(angle):
    sd.pitch(angle)
