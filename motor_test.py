import time 
import motor_driver
import smbus2

bus = smbus2.SMBus(0)
mc = motor_driver.MotorDriver(bus)

while True:
    info = input('Enter Speed and Time ')
    input_dims = info.split()
    speed = int(input_dims[0])
    dur = int(input_dims[1])
    print("speed is", speed)
    print("duration is", dur)
    mc.fwd_bwd(speed, 'fwd')
    time.sleep(dur)
    mc.stop()