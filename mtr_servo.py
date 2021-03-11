import board
import busio
import time
import adafruit_pca9685

i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)

pca.frequency = 60

mtr1_pwm = pca.channels[8]
mtr1_dir = pca.channels[9]
mtr2_pwm = pca.channels[10]
mtr2_dir = pca.channels[11]

HIGH = 0xFFFF
LOW = 0x0FFF

def fwd_bwd(self, spd, dir):
        if dir == 'fwd':
            mtr1_dir = HIGH
            mtr2_dir = LOW
        elif dir == 'bwd':
            mtr1_dir = LOW
            mtr2_dir = HIGH
        motor_speed = int(spd * 65535)
        mtr1_pwm.duty_cycle = motor_speed
        mtr2_pwm.duty_cycle = motor_speed

def pivot(self, speed, dir):
        if dir == 'left':
            mtr1_dir = HIGH
            mtr2_dir = HIGH
        elif dir == 'right':
            mtr1_dir = LOW
            mtr2_dir = LOW
        motor_speed = int(spd * 65535)
        mtr1_pwm.duty_cycle = motor_speed
        mtr2_pwm.duty_cycle = motor_speed

def stop(self):
        mtr1_pwm.duty_cycle = LOW
        mtr2_pwm.duty_cycle = LOW

while True:
    info = input('Enter Speed and Time and Direction: ')
    input_dims = info.split()
    speed = float(input_dims[0])
    dur = float(input_dims[1])
    dir = str(input_dims[2])
    print("speed is", speed)
    print("duration is", dur)
    print("direction is", dir)
    mc.motor_send(speed, dur, dir)
    time.sleep(dur)
