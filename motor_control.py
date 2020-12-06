import time
import Jetson.GPIO as GPIO


# Assuming DIR HIGH means forward and DIR LOW means backwards
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

RIGHT_MOTOR_DIR = 11    #GPIO pin to control right motor direction
LEFT_MOTOR_DIR = 13     #GPIO pin to control left motor direction

RIGHT_MOTOR = 32        #PWM pin to control right motor
LEFT_MOTOR = 33         #PWM pin to control left motor

#Initialize pins
def initialize():
    GPIO.setup(RIGHT_MOTOR_DIR, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(LEFT_MOTOR_DIR, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(RIGHT_MOTOR, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(LEFT_MOTOR, GPIO.OUT, initial = GPIO.LOW)

    pwm = [GPIO.PWM(RIGHT_MOTOR, 50), GPIO.PWM(LEFT_MOTOR, 50)]
    pwm[0].start(0)
    pwm[1].start(0)

#Move both motors forwards at speed for duration
def forward(speed, duration):
    GPIO.output(RIGHT_MOTOR_DIR, GPIO.LOW)
    GPIO.output(LEFT_MOTOR_DIR, GPIO.LOW)
    right_speed = (speed - (-1)/2)*100
    left_speed = right_speed
    pwm[0].ChangeDutyCycle(right_speed)
    pwm[1].ChangeDutyCycle(left_speed)
    time.sleep(duration)
    stop()

#Move right motor backwards, while moving left motor forwards until desired angle
def pivot_right(duration):
    GPIO.output(RIGHT_MOTOR_DIR, GPIO.HIGH)
    GPIO.output(LEFT_MOTOR_DIR, GPIO.LOW)
    pwm[0].ChangeDutyCycle(100)
    pwm[1].ChangeDutyCycle(100)
    time.sleep(duration)
    stop()

#Move right motor backwards, while moving left motor forwards until desired angle
def pivot_left(duration):
    GPIO.output(RIGHT_MOTOR_DIR, GPIO.LOW)
    GPIO.output(LEFT_MOTOR_DIR, GPIO.HIGH)
    pwm[0].ChangeDutyCycle(100)
    pwm[1].ChangeDutyCycle(100)
    time.sleep(duration)
    stop()

#Move both motors forwards at speed for duration
def backward(speed, duration):
    GPIO.output(RIGHT_MOTOR_DIR, GPIO.LOW)
    GPIO.output(LEFT_MOTOR_DIR, GPIO.LOW)
    right_speed = (speed - (-1)/2)*100
    left_speed = right_speed
    pwm[0].ChangeDutyCycle(right_speed)
    pwm[1].ChangeDutyCycle(left_speed)
    time.sleep(duration)
    stop()

#Stop both motors
def stop():
    pwm[0].ChangeDutyCycle(0)
    pwm[1].ChangeDutyCycle(1)