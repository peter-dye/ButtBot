import threading
from multiprocessing import shared_memory

lock = threading.Lock()
shm_a = shared_memory.SharedMemory(create=True, size=4)
buffer = shm_a.buf

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

shm_a.close()
shm_a.unlink()