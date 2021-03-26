# NEED TO FIGURE OUT HOW BOT PHYSICALLY MOVES TO CHANGE PARAMETERS OF MOVEMENT FUNCTIONS
# WANT TO SPECIFY DISTANCE FOR FWD BWD, AND ANGLES FOR RIGHT AND LEFT
import math
import time
from constants import SLAVE_ADDR
import busio
import board
import adafruit_pca9685
from queue import Queue
from threading import Thread
from ultrasonic_driver import UltrasonicDriver

i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)
pca.frequency = 60


class MotorDriver():

    def __init__(self):
        self.q = Queue()
        self.HIGH = 0xFFFF
        self.LOW = 0x0000
        self.mtr1_dir = pca.channels[8]
        self.mtr1_pwm = pca.channels[9]
        self.mtr2_dir = pca.channels[10]
        self.mtr2_pwm = pca.channels[11]

        self.t = Thread(target=self.motor_consume)
        self.t.start()

        self.mtr1_pwm.duty_cycle = self.LOW
        self.mtr2_pwm.duty_cycle = self.LOW

        # initialize ultrasonic sensors (process)
        self.ultrasonic_driver = UltrasonicDriver()

        return

    # Move both motors forwards at speed for duration
    def fwd_bwd(self, spd, dir):
            if dir == 'fwd':
                self.mtr1_dir.duty_cycle = self.HIGH
                self.mtr2_dir.duty_cycle = self.LOW
            elif dir == 'bwd':
                self.mtr1_dir.duty_cycle = self.LOW
                self.mtr2_dir.duty_cycle = self.HIGH
            motor_speed = int(spd * 65535)

            if spd == 0.5:
                self.mtr1_pwm.duty_cycle = motor_speed - 2500
            else:
                self.mtr1_pwm.duty_cycle = motor_speed - 6000
            
            self.mtr2_pwm.duty_cycle = motor_speed

    # Move right motor backwards, while moving left motor forwards until desired angle
    def pivot(self, spd, dir):
            if dir == 'left':
                self.mtr1_dir.duty_cycle = self.LOW
                self.mtr2_dir.duty_cycle = self.LOW
            elif dir == 'right':
                self.mtr1_dir.duty_cycle = self.HIGH
                self.mtr2_dir.duty_cycle = self.HIGH
            motor_speed = int(spd * 65535)

            # Always turn with motors half speed
            motor_speed = int(0.5 * 65535)
            self.mtr1_pwm.duty_cycle = motor_speed - 2560
            self.mtr2_pwm.duty_cycle = motor_speed

    # Stop both motors
    def stop(self):
            self.mtr1_pwm.duty_cycle = self.LOW
            self.mtr2_pwm.duty_cycle = self.LOW

    def motor_send(self, speed, distance, direction):
        data = [0,0,0]
        data[0] = speed
        
        if direction == 'fwd' or direction == 'bwd':
            data[1] = self.dist2dur(speed, distance)
        elif direction == 'right' or direction == 'left':
            data[1] = self.angle2dur(distance)
        else:
            data[1] = 0

        data[2] = direction
        self.q.put(data)

    def motor_consume(self):
        while True:
            data = self.q.get()
            print(data)
            if data[2] == 'fwd' or data[2] == 'bwd':
                self.fwd_bwd(data[0], data[2])
                end_time = time.time() + data[1]
                distances = self.ultrasonic_driver.get_distances()
                while time.time() < end_time:
                    if distances[0] > 20 and distances[1] > 20:
                        distances = self.ultrasonic_driver.get_distances()
                    else:
                        self.stop()
                time.sleep(data[1])
                self.stop()
            elif data[2] == 'right' or data[2] == 'left':
                self.pivot(data[0],data[2])
                end_time = time.time() + data[1]
                distances = self.ultrasonic_driver.get_distances()
                while distances[2] > 30 and distances[3] > 30 and time.time() < end_time:
                    distances = self.ultrasonic_driver.get_distances()
                time.sleep(data[1])
                self.stop()
            else:
                print("not a valid direction")
                self.stop()
            
    def dist2dur(self, spd, dist):
        if spd == 1:
            return (dist + 1.7357)/42.798
        elif spd == 0.5:
            return (dist + 2.05)/22.031
        else: 
            return 0

    def angle2dur(self, angle):
        return (0.0143*angle) + 0.0214
    
    def running(self):
        if self.mtr1_pwm.duty_cycle == self.LOW or self.mtr2_pwm.duty_cycle == self.LOW:
            return False
        else:
            return True
