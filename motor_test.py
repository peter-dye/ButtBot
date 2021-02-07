import RPi.GPIO as GPIO
import time

output_pin = 15

def main():
    # Pin Setup:
    # Board pin-numbering scheme
    GPIO.setmode(GPIO.BOARD)
    # set pin as an output pin with optional initial state of HIGH
    GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(13, GPIO.OUT, initial=GPIO.HIGH)
    #p = GPIO.PWM(output_pin, 50)
    #val = 100
    #incr = 100
    #p.start(val)
    while True:
        pass
    #print("PWM running. Press CTRL+C to exit.")
    #try:
    #    while True:
    #        time.sleep(3)
    #        if val >= 100:
    #            incr = -incr
    #        if val <= 0:
    #            incr = -incr
    #        val += incr
    #        p.ChangeDutyCycle(val)
    #finally:
    #    p.stop()
    #    GPIO.cleanup()

if __name__ == '__main__':
    main()
