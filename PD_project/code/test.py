import RPi.GPIO as GPIO
import time
from gpiozero import DistanceSensor

caneCount, var1Count, var2Count, var3Count, var4Count, var5Count, waitCount = 0

relay_pin3 = 23
relay_pin4 =24
var_pin1 = 14
var_pin2 = 15
var_pin3 = 18
ena_pin = 22
start_pin = 27


ultrasonic = DistanceSensor(echo=17, trigger=4)
GPIO.setmode(GPIO.BCM)


#GPIO.setup(relay_pin3, GPIO.OUT)
#GPIO.setup(relay_pin4, GPIO.OUT)
GPIO.setup(var_pin1, GPIO.OUT)
GPIO.setup(var_pin2, GPIO.OUT)
GPIO.setup(var_pin3, GPIO.OUT)
GPIO.setup(ena_pin, GPIO.OUT)
GPIO.setup(start_pin, GPIO.OUT)


var = 1 #temp variety


#functions setup
'''
def relay_ena():
     GPIO.output(relay_pin3, GPIO.HIGH) 
     GPIO.output(relay_pin4, GPIO.LOW) 
     time.sleep(5)
     GPIO.output(relay_pin3, GPIO.LOW) 
     GPIO.output(relay_pin4, GPIO.HIGH) 
     time.sleep(5)
'''
def reset_varPins():
     GPIO.output(var_pin1, GPIO.LOW)
     GPIO.output(var_pin2, GPIO.LOW)
     GPIO.output(var_pin3, GPIO.LOW)

#process start    
GPIO.output(start_pin, GPIO.HIGH) 
reset_varPins()

while True:


     #detect cane within range of camera
     if ultrasonic.distance <= 3:

          #enaPin disable
          GPIO.output(ena_pin, GPIO.LOW) 
          reset_varPins()


          #picture and ml code here
          
          
          #temp var detection
          if var == 5:
               var = 1
          else:
               var += 1
     
          
          #varPins activate, incre,ent varCount
          match var:
               case 1:
                    GPIO.output(var_pin1, GPIO.LOW)
                    GPIO.output(var_pin2, GPIO.LOW)
                    GPIO.output(var_pin3, GPIO.HIGH)
                    var1Count += 1
               case 2:
                    GPIO.output(var_pin1, GPIO.LOW)
                    GPIO.output(var_pin2, GPIO.HIGH)
                    GPIO.output(var_pin3, GPIO.LOW)
                    var2Count += 1
               case 3:
                    GPIO.output(var_pin1, GPIO.LOW)
                    GPIO.output(var_pin2, GPIO.HIGH)
                    GPIO.output(var_pin3, GPIO.HIGH)
                    var3Count += 1
               case 4:
                    GPIO.output(var_pin1, GPIO.HIGH)
                    GPIO.output(var_pin2, GPIO.LOW)
                    GPIO.output(var_pin3, GPIO.LOW)
                    var4Count += 1
               case 5:
                    GPIO.output(var_pin1, GPIO.HIGH)
                    GPIO.output(var_pin2, GPIO.LOW)
                    GPIO.output(var_pin3, GPIO.HIGH)
                    var5Count += 1
          caneCount +=1
          #enaPin enable
          GPIO.output(ena_pin, GPIO.HIGH) 

          print("cane #"+str(caneCount)+" Variety:"+str(var)+
                "\nVariety 1:"+str(var1Count)+
                "\nVariety 2:"+str(var2Count)+
                "\nVariety 3:"+str(var3Count)+
                "\nVariety 4:"+str(var4Count)+
                "\nVariety 5:"+str(var5Count))
     else:
          time.sleep(1)
          waitCount += 1
     
     if waitCount >= 10:
          GPIO.output(start_pin, GPIO.LOW)
          print("No Cane Detected.\nSUMMARY\nTotal Cane: "+str(caneCount)+
                "\nVariety 1:"+str(var1Count)+
                "\nVariety 2:"+str(var2Count)+
                "\nVariety 3:"+str(var3Count)+
                "\nVariety 4:"+str(var4Count)+
                "\nVariety 5:"+str(var5Count)+
                "Process End")
          break 




