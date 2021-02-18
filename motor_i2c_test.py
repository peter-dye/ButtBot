import motor_i2c_control
import smbus2

bus = smbus2.SMBus(1)
mc = motor_i2c_control.MotorDriver(bus)

def forward():
	mc.fwd_bwd(1, 2, 'fwd')

def backward():
	mc.fwd_bwd(1, 2, 'bwd')

def right():
	mc.pivot(1, 2, 'right')

def left():
	mc.pivot(1,2, 'left')

while true:
	text = input("Enter direction: ")

	if text == 'fwd':
		forward()
	elif text == 'bwd':
		backward()
	elif text == 'right':
		right()
	elif text == 'left':
		left()