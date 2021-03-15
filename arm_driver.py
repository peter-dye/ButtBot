import board
import digitalio
from pinout import FAN, ARM
from time import sleep

arm = digitalio.DigitalInOut(board.D26)
arm.direction = digitalio.Direction.OUTPUT

class Arm():

    def __init__(self):#, queue):
        #GPIO.setup(FAN, GPIO.OUT, initial=GPIO.LOW)
        self.state = 'down'
        #self.q = queue

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
        sleep(3)
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
        arm.value = True
        self.state = 'up'
        
    def down(self):
        arm.value = False
        self.state = 'down'

    def arm_send(self, method):
        self.q.put(method)
    
    def arm_consume(self):
        while True:
            method = self.q.get()
            if method == 'up':
                arm.up()
            elif method == 'down':
                arm.down()
            elif method == 'pickup':
                arm.pickup()
            else:
                print("Not a valid arm function!")

arm = Arm()
arm.up()
arm.down()
sleep(10)