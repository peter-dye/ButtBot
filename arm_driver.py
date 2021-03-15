import board
import digitalio
from time import sleep

ARM = digitalio.DigitalInOut(board.D26)
ARM.direction = digitalio.Direction.OUTPUT

class Arm():

    def __init__(self):#, queue):
        ARM.value = False
        self.state = 'down'
        #self.q = queue

    def pickup(self):
        # turn on fan
        GPIO.output(FAN, GPIO.HIGH)
        # lower arm
        ARM.value = False
        # wait for fan to hit full speed and pickup butt
        sleep(8)       
        # raise arm
        ARM.value = True
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
        ARM.value = True
        self.state = 'up'
        
    def down(self):
        ARM.value = False
        self.state = 'down'

    def arm_send(self, method):
        self.q.put(method)
    
    def arm_consume(self):
        while True:
            method = self.q.get()
            if method == 'up':
                self.up()
            elif method == 'down':
                self.down()
            elif method == 'pickup':
                self.pickup()
            else:
                print("Not a valid arm function!")

arm = Arm()
arm.up()
sleep(5)
arm.down()
sleep(5)