import Jetson.GPIO as GPIO
from pinout import FAN, ARM
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(FAN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ARM, GPIO.OUT, initial=GPIO.LOW)

GPIO.output(FAN, GPIO.HIGH)
time.sleep(8)
GPIO.output(ARM, GPIO.HIGH)

time.sleep(5)
GPIO.output(FAN, GPIO.LOW)
time.sleep(1)
GPIO.output(ARM, GPIO.LOW)
