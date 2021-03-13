import Jetson.GPIO as GPIO
from pinout import FAN
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(FAN, GPIO.OUT, initial=GPIO.LOW)
time.sleep(3)
GPIO.output(FAN, GPIO.HIGH)
print("Fan on")
time.sleep(10)
GPIO.output(FAN, GPIO.LOW)
print("Fan off")