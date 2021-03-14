import Jetson.GPIO as GPIO
from pinout import FAN, ARM
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

class Arm():

    def __init__(self):
        GPIO.setup(FAN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(ARM, GPIO.OUT, initial=GPIO.LOW)
        self.state = 'down'

    def pickup(self):
        # turn on fan
        GPIO.output(FAN, GPIO.HIGH)
        # lower arm
        GPIO.output(ARM, GPIO.LOW)
        # wait for fan to hit full speed and pickup butt
        sleep(8)       
        # raise arm
        GPIO.output(ARM, GPIO.HIGH)
        #wait for arm to raise
        time.sleep(3)
        # turn off fan
        GPIO.output(FAN, GPIO.LOW)
        # wait for butt to fall
        sleep(1)
        # return arm to prev state
        if self.state == 'up':
            self.up()
        else:
            self.down()

    def up(self):
        GPIO.output(ARM, GPIO.HIGH)
        self.state = 'up'
        
    def down(self):
        GPIO.output(ARM, GPIO.LOW)
        self.state = 'down'
       
arm = Arm()
while True:
    ind = input('>>>')
    if ind == 'up':
        arm.up()
    elif ind == 'down':
        arm.down()
    elif ind == 'pickup':
        arm.pickup()
    else:
        break
GPIO.cleanup()