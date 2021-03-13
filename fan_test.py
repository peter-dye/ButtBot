import Jetson.GPIO as GPIO
from pinout import FAN
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(FAN, GPIO.OUT, initial=GPIO.HIGH)
time.sleep(3)
GPIO.output(FAN, GPIO.LOW)
print("LOW")
time.sleep(10)
GPIO.output(FAN, GPIO.HIGH)
print("Back high")