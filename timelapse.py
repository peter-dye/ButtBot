from motor_driver import MotorDriver
from arm_driver import ArmDriver
from servo_driver import ServoDriver
import time
import random as r

md = MotorDriver()
sd = ServoDriver()
ad = ArmDriver()

while True:
    dur = r.randint(1,5)
    print("dur is", dur)
    speed = r.uniform(0.1,1)
    print("speed is ", speed)
    md.motor_send(speed, dur, 'fwd')
    time.sleep(dur)

    func = r.randint(1,3)
   
    if func == 1:
        sub_func = r.randint(1,2)
        if sub_func == 1:
            if ad.state == 'up':
                ad.down()
            else:
                ad.up()
        else:
            ad.pickup()
    elif func == 2:
        sub_func = r.randint(1,2)
        if sub_func == 1:
            ang = r.randint(-180,180)
            sd.pan(ang)
        else:
            ang = r.randint(0,126)
            sd.pitch(ang)
    time.sleep(5)