import time
from pins import Pins



class Varqueue():
    def __init__(self):
        self.pins = Pins(25,8,7, 23,24, 14,15, 12)
        self.pins.all_pin_low()
        self.queues = []
    
    def add(self,var):
        self.queues.append(var)
        out = self.queues[0]
        self.pins.out_to_pins(out)
           
    def loop(self):
        while True:
            if self.pins.readDoor() == 0:
                if len(self.queues)>1:    
                    self.queues.pop(0)
                    out = self.queues[0]
                    self.pins.out_to_pins(out)
                while self.pins.readDoor() == 0:
                    pass
                time.sleep(1)      
        
