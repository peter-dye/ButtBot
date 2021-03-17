import board
import digitalio
from time import sleep
from queue import Queue
from threading import Thread


class ArmDriver():

    def __init__(self):
        self.state = 'down'
        # self.q = Queue()
        # self.t = Thread(target=self.consume)
        # self.t.start()

        self.ARM = digitalio.DigitalInOut(board.D26)
        self.ARM.direction = digitalio.Direction.OUTPUT
        self.ARM.value = False

        self.FAN = digitalio.DigitalInOut(board.D19)
        self.FAN.direction = digitalio.Direction.OUTPUT
        self.FAN.value = False

    def pickup(self):
        # turn on fan
        self.FAN.value = True
        # lower arm
        self.ARM.value = False
        # wait for fan to hit full speed and pickup butt
        sleep(8)
        # raise arm
        self.ARM.value = True
        #wait for arm to raise
        sleep(3)
        # turn off fan
        self.FAN.value = False
        # wait for butt to fall
        sleep(1)
        # return arm to prev state
        if self.state == 'up':
            self.up()
        else:
            self.down()

    def up(self):
        print('in up')
        self.ARM.value = True
        self.state = 'up'

    def down(self):
        self.ARM.value = False
        self.state = 'down'

    def send(self, method):
        self.q.put(method)

    def consume(self):
        while True:
            method = self.q.get()
            if method == 'up':
                print("sending up command")
                self.up()
            elif method == 'down':
                self.down()
            elif method == 'pickup':
                self.pickup()
            else:
                print("Not a valid arm function!")
