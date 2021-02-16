import RPi.GPIO as GPIO
import time

output_pin = 33

def main():
    # Pin Setup:
    # Board pin-numbering scheme
    GPIO.setmode(GPIO.BOARD)
    # set pin as an output pin with optional initial state of HIGH
    GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(15, GPIO.OUT, initial=GPIO.HIGH)
    p = GPIO.PWM(output_pin, 50)
    val = 100
    incr = 100
    p.start(val)
    while True:
        print("PWM running. Press CTRL+C to exit.")
        GPIO.output(15, GPIO.LOW)
        p.ChangeDutyCycle(100)
        time.delay(3)
        p.ChangeDutyCycle(50)
        time.delay(3)
        GPIO.output(15, GPIO.HIGH)
        time.delay(3)
        p.ChangeDutyCycle(100)

if __name__ == '__main__':
    main()
