import threading
from multiprocessing import Process, Array

lock = threading.Lock()
buffer = Array('I', range(4))
shm_a = Process()
shm_a.start()

def write_to_mem(buffer, lock):
	lock.acquire()
	for i in range(4):
		buffer[i] = i
	lock.release()
		
def read_from_mem(buffer,lock):
	lock.acquire()
	for i in range(4):
		print("buffer index ",i, "is", buffer[i])
	lock.release()


write_to_mem(buffer,lock)
read_from_mem(buffer,lock)

shm_a.terminate()
