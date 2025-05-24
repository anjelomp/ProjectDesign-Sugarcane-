import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Pins:
    #Pins(varpin1, varpin2, varpin3, enable, start, conveyor, magnetic door, feeder)
    def __init__(self, pin1, pin2, pin3, enable, start, ir, door, feeder):
        self.pin1 = pin1
        self.pin2 = pin2
        self.pin3 = pin3
        self.enable = enable
        self.start = start
        self.ir = ir
        self.door = door
        self.feeder = feeder
        GPIO.setup(self.pin1, GPIO.OUT)
        GPIO.setup(self.pin2, GPIO.OUT)
        GPIO.setup(self.pin3, GPIO.OUT)
        GPIO.setup(self.enable, GPIO.IN)
        GPIO.setup(self.start, GPIO.OUT)
        GPIO.setup(self.ir, GPIO.IN)
        GPIO.setup(self.door, GPIO.IN)
        GPIO.setup(self.feeder, GPIO.OUT)
       


    
    def all_pin_low(self):
        GPIO.output(self.pin1, GPIO.LOW)
        GPIO.output(self.pin2, GPIO.LOW)
        GPIO.output(self.pin3, GPIO.LOW)
        GPIO.output(self.start, GPIO.LOW)
        GPIO.output(self.feeder, GPIO.LOW)


    def reset_varPins(self):
        GPIO.output(self.pin1, GPIO.LOW)
        GPIO.output(self.pin2, GPIO.LOW)
        GPIO.output(self.pin3, GPIO.LOW)

    def out_to_pins(self, var):
        match var:
            case 1:
                GPIO.output(self.pin3, GPIO.LOW)
                GPIO.output(self.pin2, GPIO.LOW)
                GPIO.output(self.pin1, GPIO.HIGH)
                
            case 2:
                GPIO.output(self.pin3, GPIO.LOW)
                GPIO.output(self.pin2, GPIO.HIGH)
                GPIO.output(self.pin1, GPIO.LOW)
                
            case 3:
                GPIO.output(self.pin3, GPIO.LOW)
                GPIO.output(self.pin2, GPIO.HIGH)
                GPIO.output(self.pin1, GPIO.HIGH)
                
            case 4:
                GPIO.output(self.pin3, GPIO.HIGH)
                GPIO.output(self.pin2, GPIO.LOW)
                GPIO.output(self.pin1, GPIO.LOW)
                 
            case 5:
                GPIO.output(self.pin3, GPIO.HIGH)
                GPIO.output(self.pin2, GPIO.LOW)
                GPIO.output(self.pin1, GPIO.HIGH)
    

    def readEnable(self):
        return GPIO.input(self.enable)

    def start_low(self):
        GPIO.output(self.start, GPIO.LOW)
    def start_high(self):
        GPIO.output(self.start, GPIO.HIGH)
    
    def readIR(self):
        return GPIO.input(self.ir)

    def readDoor(self):
        return GPIO.input(self.door)
        
    def feeder_start(self):
        GPIO.output(self.feeder, GPIO.HIGH)
    def feeder_stop(self):
        GPIO.output(self.feeder, GPIO.LOW)


