import array
import sys
import time
import RPi.GPIO as GPIO
import threading

from stepper import Stepper
from gpiozero import DistanceSensor
from pins import Pins
from camera import Camera
from stepact import StepAct
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)



try:
    #Pins(varpin1, varpin2, varpin3, enable, start, conveyor, magnetic door, feeder)

    pins = Pins(25,8,7, 23,24, 14,15, 12)
    

    #camera setup
 
 
    cam = Camera(0)
    cam.start_camera()


    print("\n\nSetup Complete. Proceed?\n")
    input()  

except Exception as e:
    print(f"Setup failed. Exiting program. Error {e}")
    sys.exit()

while True:
    try:
        
        while True:
            print("-----------r1 pins---------")

            ans = input("proceed? y/n\n")
            if ans == "n":
                break

            pins.all_pin_low()
            print("all pins low")
            input()

            pins.out_to_pins(1)
            print("var = 1")
            input()

            pins.out_to_pins(2)
            print("var = 2")
            input()

            pins.out_to_pins(3)
            print("var = 3")
            input()

            pins.out_to_pins(4)
            print("var = 4")
            input()

            pins.out_to_pins(5)
            print("var = 5")
            input()

            pins.reset_varPins()
            print("reset var")
            input()

            pins.start_high()
            print("start high")
            input()

            pins.start_low()
            print("start_low")
            input()

            ans = input('Repeat? y/n\n')

            if ans == "n":
                break


        while True:

            print("-----------sensor---------")

            ans = input("proceed? y/n\n")
            if ans == "n":
                break

            for i in range(20):

                print("IR | Door")
                print(pins.readIR())
                print(pins.readDoor())
                time.sleep(1)    

            ans = input('repeat? y/n\n')

            if ans == "n":
                break


        while True:

            print("-----------feeder---------")

            ans = input("proceed? y/n\n")
            if ans == "n":
                break

            print("Feeder Running")
            pins.feeder_start()
            input()

            print("Feeder Stop")
            pins.feeder_stop()
            input()

            ans = input('Repeat? y /n\n')

            if ans == "n":
                break


    except Exception as e:
        print(f"error. {e}")
        input()
