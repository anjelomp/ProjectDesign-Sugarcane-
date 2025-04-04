import time

class Timeout():
    def __init__(self,  *args, **kwargs):
        self.time = 0

    def timer_init(self):
        while self.start:
            time.sleep(1)
            self.time += 1
    
    def start(self):
        self.start = True
    def stop(self):
        self.start = False
    def reset(self):
        self.time = 0
    def get(self):
        return self.time