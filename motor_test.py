import RPi.GPIO as GPIO
import time

output_pin = 33

def main():
    # Pin Setup:
    # Board pin-numbering scheme
    GPIO.setmode(GPIO.BOARD)
    # set pin as an output pin with optional initial state of HIGH
    GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(19, GPIO.OUT, initial=GPIO.HIGH)
    p = GPIO.PWM(output_pin, 50)
    p.start(0)
    #while True:
    #    print("DIR HIGH, FULL SPEED")
    #    p.ChangeDutyCycle(100)
    #    time.sleep(5)
    #    print("DIR HIGH, HALF SPEED")
    #    p.ChangeDutyCycle(50)
    #    time.sleep(5)
    #    print("DIR HIGH, 0 SPEED")
    #    p.ChangeDutyCycle(50)
    #    time.sleep(5)
    #    print("DIR LOW, HALF SPEED")
    #    GPIO.output(15, GPIO.LOW)
    #    time.sleep(5)
    #    print("DIR LOW, FULL SPEED")
    #    p.ChangeDutyCycle(100)
    #    time.sleep(5)

    while True:
        print("PWM PIN HIGH, Should be direction A")
        p.ChangeDutyCycle(100)
        time.sleep(5)
        print("PWM PIN HIGH, Should be direction B")
        p.ChangeDutyCycle(0)
        time.sleep(5)
        print("PWM PIN HIGH, Should be stopped")
        p.ChangeDutyCycle(50)
        time.sleep(3)

if __name__ == '__main__':
    main()
