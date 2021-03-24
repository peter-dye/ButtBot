"""
This is the entry point to running the entire ButtBot system.
"""

from motor_driver import MotorDriver
from arm_driver import ArmDriver
from servo_driver import ServoDriver
from jetcam.csi_camera import CSICamera
from localizer import Localizer
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
        self.num_rows = int(ss_l / g_dim)
        self.num_cols = int(ss_wd / g_dim)

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
        self.path = PathPlanning(self.num_rows, self.num_cols, obstacles)

        # get vehicle commands 
        self.commands = path.get_instructions
        self.nodes = path.coordinate_list
        self.current_node = self.nodes.pop(0)
        self.next_node = self.nodes.pop(0)

        # create var for returning after butt pickup
        self.turn1 = None
        self.turn2 = None
        self.dist1 = None
        self.dist2 = None
        self.angle1 = None
        self.angle2 = None

        # initialize the state function mapping
        self.state_functions = {"first_state": self.first_state}
        self.state_functions['pickup_state'] = self.pickup_state
        self.state_functions['approach_state'] = self.approach_state
        self.state_functions['localize_state'] = self.localize_state
        self.state_functions['traverse_state'] = self.traverse_state
        self.state_functions['after_pickup_return_state'] = self.after_pickup_return_state
        self.state_functions['return_home_state'] = self.return_home_state

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
    
    def approach_state(self):
        # calculate butt relative distance
        relative_directions = RelativeButt()
        self.angle1 = relative_directions[1]
        self.dist1 = relative_directions[0]/2

        # approach but stop halfway
        if turn < 0:
            self.motor_driver.motor_send(1,self.turn1, 'left')
            self.turn1 = 'left'
        else:
            self.motor_driver.motor_send(1,self.turn1,'right')
            self.turn1 = 'right'
        self.motor_driver.motor_send(1, self.dist1, 'fwd')
        
        # recalculate
        relative_directions = RelativeButt()
        self.angle2 = relative_directions[1]
        self.dist2 = relative_directions[0]
        # finish approach
        if turn < 0:
            self.motor_driver.motor_send(1,self.turn2, 'left')
            self.turn2 = 'left'
        else:
            self.motor_driver.motor_send(1,self.turn2,'right')
            self.turn2 = 'right'
        self.motor_driver.motor_send(0.5, self.dist2, 'fwd')

        self.state = "pickup_state"
        return

    
    def pickup_state(self):
        self.arm_driver.pickup()
        self.state = localize_state
        self.state = "after_pickup_return_state"
        return

    def after_pickup_return_state(self):
        self.motor_driver.motor_send(0.5, self.dist2, 'bwd')
        if self.turn2 == 'left':
            self.motor_driver.motor_send(1, self.angle2, 'right')
        else:
            self.motor_driver.motor_send(1, self.angle2, 'left')

        self.motor_driver.motor_send(1, self.dist1, 'bwd')

        if self.turn1 == 'left':
            self.motor_driver.motor_send(1, self.angle1, 'right')
        else:
            self.motor_driver.motor_send(1, self.angle1, 'left')
        
        self.state = 'localize_state'

        return

    def traverse_state(self):
        while True:
            if self.commands is empty:
                break
            command = self.commands.pop(0)
            if command > 1:
                self.motor_driver.motor_send(1, command, 'right')
            elif command < 0:
                self.motor_driver.motor_send(1, command, 'left')
            else:
                self.motor_driver.send(1, length_of_bb, 'fwd') ##NEED TO ADD AND UPDATE
                self.current_node = self.next_node
                self.next_node = self.path.pop(0)
                break
        if self.nodes is empty:
            self.state = 'return_home_state'
        else:
            self.state = "traverse_state"
        return

        def return_home_state(self):    
            home_path = self.path.path_home
            home_instructions = self.path.instructions_home
            #self.current_node = home_path.pop(0)
            while True:
                if self.commands is empty:
                    break
                command = self.home_instructions.pop(0)
                if command > 1:
                    self.motor_driver.motor_send(1, command, 'right')
                elif command < 0:
                    self.motor_driver.motor_send(1, command, 'left')
                else:
                    self.motor_driver.send(1, length_of_bb, 'fwd') ##NEED TO ADD AND UPDATE
            return
 