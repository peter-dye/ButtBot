# NEED TO FIGURE OUT HOW BOT PHYSICALLY MOVES TO CHANGE PARAMETERS OF MOVEMENT FUNCTIONS
# WANT TO SPECIFY DISTANCE FOR FWD BWD, AND ANGLES FOR RIGHT AND LEFT

import time
import Jetson.GPIO as GPIO


class Motor_Driver():

    def __init__(self):
        # initialize pins
        self.RIGHT_MOTOR_DIR = 11    # GPIO pin to control right motor direction
        self.LEFT_MOTOR_DIR = 13     # GPIO pin to control left motor direction

        self.RIGHT_MOTOR = 32        # PWM pin to control right motor
        self.LEFT_MOTOR = 33         # PWM pin to control left motor

        # Assuming DIR HIGH means forward and DIR LOW means backwards
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.RIGHT_MOTOR_DIR, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.LEFT_MOTOR_DIR, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.RIGHT_MOTOR, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.LEFT_MOTOR, GPIO.OUT, initial=GPIO.LOW)

        self.pwm = [GPIO.PWM(self.RIGHT_MOTOR, 50), GPIO.PWM(self.LEFT_MOTOR, 50)]
        self.pwm[0].start(0)
        self.pwm[1].start(0)

    # Move both motors forwards at speed for duration
    def fwd(self, spd, dur):
        GPIO.output(self.RIGHT_MOTOR_DIR, GPIO.LOW)
        GPIO.output(self.LEFT_MOTOR_DIR, GPIO.LOW)
        right_speed = (spd - (-1)/2)*100
        left_speed = right_speed
        self.pwm[0].ChangeDutyCycle(right_speed)
        self.pwm[1].ChangeDutyCycle(left_speed)
        time.sleep(dur)
        self.stop()

    # Move right motor backwards, while moving left motor forwards until desired angle
    def pivot_right(self, dur):
        GPIO.output(self.RIGHT_MOTOR_DIR, GPIO.HIGH)
        GPIO.output(self.LEFT_MOTOR_DIR, GPIO.LOW)
        self.pwm[0].ChangeDutyCycle(100)
        self.pwm[1].ChangeDutyCycle(100)
        time.sleep(dur)
        self.stop()

    # Move right motor backwards, while moving left motor forwards until desired angle
    def pivot_left(self, dur):
        GPIO.output(self.RIGHT_MOTOR_DIR, GPIO.LOW)
        GPIO.output(self.LEFT_MOTOR_DIR, GPIO.HIGH)
        self.pwm[0].ChangeDutyCycle(100)
        self.pwm[1].ChangeDutyCycle(100)
        time.sleep(dur)
        self.stop()

    # Move both motors forwards at speed for duration
    def bwd(self, spd, dur):
        GPIO.output(self.RIGHT_MOTOR_DIR, GPIO.LOW)
        GPIO.output(self.LEFT_MOTOR_DIR, GPIO.LOW)
        right_speed = (spd - (-1)/2)*100
        left_speed = right_speed
        self.pwm[0].ChangeDutyCycle(right_speed)
        self.pwm[1].ChangeDutyCycle(left_speed)
        time.sleep(dur)
        self.stop()

    # Stop both motors
    def stop(self):
        self.pwm[0].ChangeDutyCycle(0)
        self.pwm[1].ChangeDutyCycle(0)
