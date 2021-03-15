def put_cmd(q):
	info = input('Enter Speed and Time and Direction: ')
	input_dims = info.split()
	speed = float(input_dims[0])
	dur = float(input_dims[1])
	dir = str(input_dims[2])
	arm = str(input_dims[3])
	data = [speed, dur, dir, arm]
	q.put(data)
