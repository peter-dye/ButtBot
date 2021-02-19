import motor_i2c_control
import smbus2
import ultrasonic_driver

bus = smbus2.SMBus(0)

mc = motor_i2c_control.MotorDriver(bus)
us = ultrasonic_driver.UltrasonicDriver(bus)

def forward():
	mc.fwd_bwd(1, 2, 'fwd')

def backward():
	mc.fwd_bwd(1,2, 'bwd')

def right():
	mc.pivot(2, 'right')

def left():
	mc.pivot(2, 'left')

while True:
	while(readI2C(SLAVE_ADDR) < 255):   #255 is the start byte, so if we read in the middle of a transmission, wait until next start
		print("Waiting")                          
	
	for bcount in range(5):
		distance[bcount] = readI2C(SLAVE_ADDR) #Put each distance in the list in its respective position
		if(distance[bcount] < 100):
			motor_controller.stop()
			time.sleep(1)
	print("0: "+str(distance[0])+
			" 1: "+str(distance[1])+
			" 2: "+str(distance[2])+
			" 3: "+str(distance[3])+
			" 4: "+str(distance[4]))
	time.sleep(.200)                            #Delay for 200ms

	text = input("Enter direction: ")

	if text == 'fwd':
		forward()
	elif text == 'bwd':
		backward()
	elif text == 'right':
		right()
	elif text == 'left':
		left()
