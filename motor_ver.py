from motor_driver import MotorDriver

md = MotorDriver()

while True:
    info = input("Enter Speed, Time, Direction:" )
    input_dims = info.split()
    speed = float(input_dims[0])
    dur = float(input_dims[1])
    dir = str(input_dims[2])

    print(speed, dur, dir)

    md.motor_send(speed, dur, dir)
