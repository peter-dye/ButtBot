import Jetson.GPIO as GPIO
from pinout import FAN, ARM
import time
from servo_driver import arm



#GPIO.output(FAN, GPIO.HIGH)
#time.sleep(8)
#GPIO.output(ARM, GPIO.HIGH)

#time.sleep(3)
#GPIO.output(FAN, GPIO.LOW)
#time.sleep(1)
#GPIO.output(ARM, GPIO.LOW)
arm()
GPIO.cleanup()