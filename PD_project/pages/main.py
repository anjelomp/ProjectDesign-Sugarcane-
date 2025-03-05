

import RPi.GPIO as GPIO
from stepper import Stepper
from gpiozero import DistanceSensor
from pins import Pins
from camera import Camera

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


import threading

import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk 
import os

#from components import Components
from db import DbPage



# solution for pathing error
os.chdir(os.path.dirname(os.path.abspath(__file__)))



class DashboardPage(Frame):
    def __init__(self, parent, counter_vars, status_vars, imgName, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        status_vars['prompt'].set("Setting Up")      
        imgName.set("holder.jpg")


        
        try:
        
            #Pins(pin1, pin2, pin3, r1, r2, enable, start)
            self.pins = Pins(14,15,18,23,24,22,27)
            self.pins.all_pin_low()


            #motor pins/flags ena, dir, pul
            self.stepper = Stepper(11,9,10)
            
            #ultrasonic
            self.ultrasonic = DistanceSensor(echo=17, trigger=4)

            #camera setup
            self.cam = Camera(0)
            self.cam.start_camera()
  
            self.db = DbPage()
            self.db.setup()

            #intial variables

        
            status_vars['prompt'].set('Setup Successful')
            
        except Exception as e:
            status_vars['prompt'].set(f"Error {e}")

#main algorithm        
###############################################################################################

        try:
            self.var = 1 #temp
	        #start 1
            self.pins.start_high()
            self.pins.enable_low()
            self.status_vars['system'].set("Enabled")
            #self.enable = 0
	    
	        #conveyor start
            self.thread = threading.Thread(target=self.stepper.run, daemon=True)
            self.thread.start()
            self.stepper.ena_low()
            status_vars['conveyor'].set("Running")
            #self.conv = 1
            
            #relay 
            #self.act = 1
            status_vars['actuator'].set("Active")
            self.pins.relay_activate()
            status_vars['actuator'].set("Inactive")

            while True:
                

                #detect cane within range of camera
                dist = self.ultrasonic.distance 
                if dist < 1.0:
                     
                    status_vars['sensor'].set(round(dist,2))    
                    #cane count
                    i=counter_vars[0].get()
                    counter_vars[0].set(i+1)
                    
                    #capture
                    imgName.set(str(self.counter_vars[0].get())+"_cane.jpg")
                    self.cam.capture_image("images/"+self.imgname)
                    self.update_camera_placeholder()
                    self.update()
                    

                    #enaPin disable
                    self.pins.enable_low()
                    #self.enable = 0
                    
                    self.pins.reset_varPins()
                    self.status_vars['variety'].set(None)

                    #temp ML var detection 
                    #self.var detecte variety
                    if self.var == 5:
                            self.var = 1
                    else:
                            self.var += 1
                
                    #varPins activate, increment varCount

                    j=self.counter_vars[self.var]
                    self.counter_vars[self.var].set(j+1)

                    self.status_vars['variety'].set(self.var)
                    self.pins.out_to_pins(self.var)

                    #enaPin enable
                    self.pins.enable_high()
                    
                    
                    self.status_vars['actuator'].set("Active")
                    self.pins.relay_activate()
                    self.status_vars['actuator'].set("Inactive")

                    
                    self.counter_vars[6].set(0)
                    dist = None
                    self.status_vars['sensor'].set(None)

                    #self.update_disp()
                else:
                    k = self.counter_vars[6].get() #wait counter
                    self.counter_vars[6].set(k+1)

                    if self.counter_vars[6].get() == 5:
                            
                        self.status_vars['actuator'].set("Active")
                        self.pins.relay_activate()
                        self.status_vars['actuator'].set("Inactive")
      
                    #display Ultrasonic not in range. Count: #
                    self.status_vars['prompt'].set("No cane detected.")
                    #self.update()            

                    self.after(2000)
                
                if self.counter_vars[6] >= 10:
                    self.pins.start_low()
                      
                    # display 
                    self.status_vars['prompt'].set("No cane detected")
                    break 

            # Release the webcam
            self.cam.release()
            self.stepper.ena_high()
            self.status_vars['conveyor'].set("Running")


        except Exception as e:
            self.disp.grid_forget()
            self.update()
            
            self.status_vars['prompt'].set(f"Error {e}")
            #self.disp.config(text=)
            self.disp.grid(row=2, column=0)



###############################################################################################

    def setup_vars(self):

        self.imgname = "holder.jpg"
        
        self.counter_vars = [IntVar(value=0) for _ in range(7)]  # Index 0: total, 1-5: varieties
        self.status_vars = {
            'sensor': IntVar(value=0),
            'variety': IntVar(value=None),
            'conveyor': StringVar(value="Stopped"),
            'actuator': StringVar(value="Inactive"),
            'system': StringVar(value="Disabled"),
            'prompt': StringVar(value="")
        }

    
  

    # Raspberry Pi integration methods
    def update_sensor_status(self, status):
        self.status_vars['sensor'].set(status)
    
    def update_variety(self, variety):
        self.status_vars['variety'].set(variety)
    
    def increment_counter(self, variety_index=0):
        """Increment counters (0 = total, 1-5 = specific varieties)"""
        if 0 <= variety_index <= 5:
            self.counter_vars[variety_index].set(self.counter_vars[variety_index].get() + 1)
        if variety_index != 0:
            self.counter_vars[0].set(self.counter_vars[0].get() + 1)

if __name__ == "__main__":
    root = Tk()
    root.title("CaneCheck")
    root.minsize(800, 600)  
    root.geometry("1024x768")
    root.configure(bg="white")
    
    reports_page = DashboardPage(root)
    reports_page.pack(fill="both", expand=True)
    
    root.mainloop()
