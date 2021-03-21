"""
This is the entry point to running the entire ButtBot system.
"""

from motor_driver import MotorDriver
from arm_driver import ArmDriver
from servo_driver import ServoDriver
from jetcam.csi_camera import CSICamera
from localizer import Localizer
from ultrasonic_driver import UltrasonicDriver
from dijkstra import PathPlanning
import re
from constants import *
from butt_relative_distance import RelativeButt

class ButtBot():

    def __init__(self):
        # initialize motor driver
        self.motor_driver = MotorDriver()

        # initialize arm driver
        self.arm_driver = ArmDriver()

        # initialize servo driver
        self.servo_driver = ServoDriver()

        # initialize camera
        self.camera = CSICamera(
            width=320,
            height=320,
            capture_width=1080,
            capture_height=720,
            capture_fps=30
        )

        # initialize localizer
        markers = []
        self.localizer = Localizer(
            markers,
            self.camera,
            self.servo_driver,
            self.arm_driver
        )

        # initialize ultrasonic sensors (process)
        self.ultrasonic_driver = UltrasonicDriver()

        # initalize butt detection (process)

        # initialize path planning
        # user input search space dimensions
        input_dims = input('Enter length and width of search space: ')
        input_dims = input_dims.split()
        ss_l = float(input_dims[0])
        ss_w = float(input_dims[1])

        # each grid square size
        g_dim = int((max(ss_l, ss_wd)) / (max(BB_L, BB_W)))

        # calculate the number of rows and columns
        num_rows = int(ss_l / g_dim)
        num_cols = int(ss_wd / g_dim)

        print('Grid is ', num_rows-1, ' tall by ', num_cols-1, ' wide.\n')

        # user input obstacle coordinates as tuples 
        line = input('Enter location of obstacles (r,c):\n') 

        temp = re.findall(r'\d+', line) 
        res = list(map(int, temp)) 

        i = 0
        obstacles = []
        while i < len(res):
            obstacles.append((res[i],res[i+1]))
            i += 2

        # create path planning object
        path = PathPlanning()

        # get vehicle commands 
        commands = path.get_instructions

        # initialize the state function mapping
        self.state_functions = {"first_state": self.first_state}
        self.state_functions['pickup_state'] = self.pickup_state
        self.state_functions['approach_state'] = self.approach_state

        # initialize the state
        self.state = "first_state"

        return

    def state_machine(self):
        while True:
            state_function = self.state_functions[self.state]
            state_function()
        return

    def first_state(self):
        # run state code
        # update self.state if there is a transition
        return
    def pickup_state(self):
        self.arm_driver.pickup()
        self.state = 0 ##THIS NEEDS TO BE THE NEXT STATE I JUST DONT KNOW WHAT IT IS
        return
    
    def approach_state(self):
        #calculate butt relative distance
        relative_directions = RelativeButt()
        turn = relative_directions[1]
        forward = relative_directions[0]
        duration = self.motor_driver.dist2dir(full, forward)
        #approach but stop halfway
        self.motor_driver.motor_send(1, duration/2, 'fwd')
        self.motor_driver.motor_send(1, duration/2, 'fwd')
        #calculate
        relative_directions = RelativeButt()
        turn = relative_directions[1]
        forward = relative_directions[0]
        duration = self.motor_driver.dist2dir(forward)
        #approach
        self.motor_driver.motor_send(1, duration, 'fwd')

        self.state = "pickup_state"
        return
