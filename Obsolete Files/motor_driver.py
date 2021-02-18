# NEED TO FIGURE OUT HOW BOT PHYSICALLY MOVES TO CHANGE PARAMETERS OF MOVEMENT FUNCTIONS
# WANT TO SPECIFY DISTANCE FOR FWD BWD, AND ANGLES FOR RIGHT AND LEFT

import time
import Jetson.GPIO as GPIO
from pinout import R_MTR, R_MTR_DIR, L_MTR, L_MTR_DIR


class MotorDriver():

    def __init__(self):
        # initialize pins
        self.R_MTR_DIR = R_MTR_DIR   # GPIO pin to control right motor direction
        self.L_MTR_DIR = L_MTR_DIR   # GPIO pin to control left motor direction

        self.R_MTR = R_MTR        # PWM pin to control right motor
        self.L_MTR = L_MTR         # PWM pin to control left motor

        # Assuming DIR HIGH means forward and DIR LOW means backwards
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.R_MTR_DIR, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.L_MTR_DIR, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.R_MTR, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.L_MTR, GPIO.OUT, initial=GPIO.LOW)

        self.pwm = [GPIO.PWM(self.R_MTR, 50), GPIO.PWM(self.L_MTR, 50)]
        self.pwm[0].start(0)
        self.pwm[1].start(0)

    # Move both motors forwards at speed for duration
    def fwd_bwd(self, spd, dur, dir):
        if dir == 'fwd':
            GPIO.output(self.R_MTR_DIR, GPIO.LOW)
            GPIO.output(self.L_MTR_DIR, GPIO.LOW)
        if dir == 'bwd':
            GPIO.output(self.R_MTR_DIR, GPIO.LOW)
            GPIO.output(self.L_MTR_DIR, GPIO.LOW)

        right_speed = ((spd - (-1))/2)*100
        left_speed = right_speed
        self.pwm[0].ChangeDutyCycle(100)
        self.pwm[1].ChangeDutyCycle(100)
        time.sleep(dur)
        self.stop()

    # Move right motor backwards, while moving left motor forwards until desired angle
    def pivot_right_left(self, dur, dir):
        if dir == 'right':
            GPIO.output(self.R_MTR_DIR, GPIO.HIGH)
            GPIO.output(self.L_MTR_DIR, GPIO.LOW)
        if dir == 'left':
            GPIO.output(self.R_MTR_DIR, GPIO.LOW)
            GPIO.output(self.L_MTR_DIR, GPIO.HIGH)
        self.pwm[0].ChangeDutyCycle(100)
        self.pwm[1].ChangeDutyCycle(100)
        time.sleep(dur)
        self.stop()

    # Stop both motors
    def stop(self):
        self.pwm[0].ChangeDutyCycle(0)
        self.pwm[1].ChangeDutyCycle(0)

