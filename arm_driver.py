import board
import digitalio
from time import sleep

class Arm():

    def __init__(self):#, queue):
        self.state = 'down'
        #self.q = queue

        ARM = digitalio.DigitalInOut(board.D26)
        ARM.direction = digitalio.Direction.OUTPUT
        ARM.value = False

        FAN = digitalio.DigitalInOut(board.D19)
        FAN.direction = digitalio.Direction.OUTPUT
        FAN.value = False

    def pickup(self):
        # turn on fan
        FAN.value = True
        # lower arm
        ARM.value = False
        # wait for fan to hit full speed and pickup butt
        sleep(8)       
        # raise arm
        ARM.value = True
        #wait for arm to raise
        sleep(3)
        # turn off fan
        FAN.value = False
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
arm.pickup()
sleep(5)