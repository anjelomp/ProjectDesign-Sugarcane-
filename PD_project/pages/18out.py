from pins import Pins



class varQueue():
    def __init__(self):
        self.pins = Pins(25,8,7, 23,24, 14,15, 12)
        self.pins.all_pin_low()
        self.queue = []
    
    def add(self,var):
        self.queue.append(var)
        out = self.queue[0]
        self.pins.out_to_pins(out)
           
    def loop(self):
        if self.pins.readDoor() == 0:
            if len(self.queue)>1:    
                self.queue.pop(0)
                out = self.queue[0]
                self.pins.out_to_pins(out)
            
            
        
