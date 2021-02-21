import time 
import threading

class ThreadingExample():
    def __init__(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        print("motor command sent")
        time.sleep(1)
        print("XXAFFWEFHFAKJFGSDFKAFDFSHGEWTQWRDA DONE")

example = ThreadingExample()
while not exit:
    print("US Data")