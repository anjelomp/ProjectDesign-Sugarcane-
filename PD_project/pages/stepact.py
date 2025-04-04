import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class StepAct:
    
    def __init__(self, ena, dirc, pul,speed,r1,r2):
        self.ena = ena
        self.dirc = dirc
        self.pul = pul
        self.speed  = speed
        self.r1 = r1
        self.r2 = r2
        GPIO.setup(self.r1, GPIO.OUT)
        GPIO.setup(self.r2, GPIO.OUT)
        GPIO.setup(self.ena, GPIO.OUT)
        GPIO.setup(self.dirc, GPIO.OUT)
        GPIO.setup(self.pul, GPIO.OUT)

    def loop(self, stat):
        self.loop = stat
        
    
    def run(self):
        GPIO.output(self.r1, GPIO.LOW) 
        GPIO.output(self.r2, GPIO.HIGH) 
        self.r1, self.r2 = self.r2, self.r1
        tTime = 0

        while self.loop:
            GPIO.output(self.pul, GPIO.HIGH)
            time.sleep(self.speed)
            
            tTime += self.speed
            if tTime == 5:
                GPIO.output(self.r1, GPIO.LOW) 
                GPIO.output(self.r2, GPIO.HIGH) 
                self.r1, self.r2 = self.r2, self.r1
                tTime = 0
            
            GPIO.output(self.pul, GPIO.LOW)
            time.sleep(self.speed)

            tTime += self.speed
            if tTime == 5:
                GPIO.output(self.r1, GPIO.LOW) 
                GPIO.output(self.r2, GPIO.HIGH) 
                self.r1, self.r2 = self.r2, self.r1
                tTime = 0

    def act_extend(self):
        GPIO.output(self.r1, GPIO.LOW) 
        GPIO.output(self.r2, GPIO.HIGH) 

    def act_close(self):
        GPIO.output(self.r1, GPIO.HIGH) 
        GPIO.output(self.r2, GPIO.LOW) 


    def dir_low(self):
        GPIO.output(self.dirc, GPIO.LOW)
    
    def dir_high(self):
        GPIO.output(self.dirc, GPIO.HIGH)

    def ena_low(self):
        GPIO.output(self.ena, GPIO.LOW)
    
    def ena_high(self):
        GPIO.output(self.ena, GPIO.HIGH)
