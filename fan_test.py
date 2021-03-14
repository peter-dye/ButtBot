import Jetson.GPIO as GPIO
from pinout import FAN, ARM
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(FAN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ARM, GPIO.OUT, initial=GPIO.LOW)

def arm():
    if GPIO.input(ARM):
        temp = GPIO.HIGH
    else:
        temp = GPIO.LOW
# turn on fan
    GPIO.output(FAN, GPIO.HIGH)
# lower arm
    GPIO.output(ARM, GPIO.LOW)
# wait 
    sleep(8)       
# raise arm
    GPIO.output(ARM, GPIO.HIGH)
# turn off fan
    GPIO.output(FAN, GPIO.LOW)
# wait
    sleep(1)
# return arm to prev state
    GPIO.output(ARM, temp)


#GPIO.output(FAN, GPIO.HIGH)
#time.sleep(8)
#GPIO.output(ARM, GPIO.HIGH)

#time.sleep(3)
#GPIO.output(FAN, GPIO.LOW)
#time.sleep(1)
#GPIO.output(ARM, GPIO.LOW)

arm()

GPIO.cleanup()