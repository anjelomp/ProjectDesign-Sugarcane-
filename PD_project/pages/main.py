

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
from ml import MachineLearning



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

            #setup ML weights
            self.ml = MachineLearning
            self.ml.setup()

        
            status_vars['prompt'].set('Setup Successful')
            
        except Exception as e:
            status_vars['prompt'].set(f"Error {e}")

#main algorithm        
###############################################################################################

        try:
            #self.var = 1 #temp
	        #start 1
            self.pins.start_high()
            self.pins.enable_low()
            status_vars['system'].set("Enabled")
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
                    
                    counter_vars[0].set(counter_vars[0].get()+1)
                    
                    #capture
                    imgName.set(str(counter_vars[0].get())+"_cane.jpg")
                    self.cam.capture_image("images/"+self.imgname)
                    self.update_camera_placeholder()
                    self.update()
                    

                    #enaPin disable
                    self.pins.enable_low()
                    #self.enable = 0
                    
                    self.pins.reset_varPins()
                    status_vars['variety'].set(None)

                    '''' 
                    #temp ML var detection 
                    #self.var detecte variety
                                   
                    if self.var == 5:
                            self.var = 1
                    else:
                            self.var += 1'''
                    
                    #ML Detection
                    self.var = self.ml.predict("images/"+self.imgname)
                
                    #varPins activate, increment varCount

                    counter_vars[self.var].set(counter_vars[self.var].get()+1)

                    status_vars['variety'].set(self.var)
                    self.pins.out_to_pins(self.var)

                    #enaPin enable
                    self.pins.enable_high()
                    
                    
                    status_vars['actuator'].set("Active")
                    self.pins.relay_activate()
                    status_vars['actuator'].set("Inactive")

                    
                    counter_vars[6].set(0)
                    dist = None
                    status_vars['sensor'].set(None)

                    #self.update_disp()
                else:

                    counter_vars[6].set(counter_vars[6].get()+1)

                    if counter_vars[6].get() == 5:
                            
                        status_vars['actuator'].set("Active")
                        self.pins.relay_activate()
                        status_vars['actuator'].set("Inactive")
      
                    #display Ultrasonic not in range. Count: #
                    status_vars['prompt'].set("No cane detected.")
                    #self.update()            

                    self.after(2000)
                
                if counter_vars[6].get() >= 10:
                    self.pins.start_low()
                      
                    # display 
                    status_vars['prompt'].set("No cane detected")
                    break 

            # Release the webcam
            self.cam.release()
            self.stepper.ena_high()
            status_vars['conveyor'].set("Running")


        except Exception as e:
            self.disp.grid_forget()
            self.update()
            
            status_vars['prompt'].set(f"Error {e}")
            #self.disp.config(text=)
            self.disp.grid(row=2, column=0)



###############################################################################################

    def setup_vars(self):

        self.imgname = "holder.jpg"
        
        counter_vars = [IntVar(value=0) for _ in range(7)]  # Index 0: total, 1-5: varieties
        status_vars = {
            'sensor': IntVar(value=0),
            'variety': IntVar(value=None),
            'conveyor': StringVar(value="Stopped"),
            'actuator': StringVar(value="Inactive"),
            'system': StringVar(value="Disabled"),
            'prompt': StringVar(value="")
        }

    
  
    '''
    # Raspberry Pi integration methods
    def update_sensor_status(self, status):
        status_vars['sensor'].set(status)
    
    def update_variety(self, variety):
        status_vars['variety'].set(variety)
    
    def increment_counter(self, variety_index=0):
        """Increment counters (0 = total, 1-5 = specific varieties)"""
        if 0 <= variety_index <= 5:
            counter_vars[variety_index].set(counter_vars[variety_index].get() + 1)
        if variety_index != 0:
            counter_vars[0].set(counter_vars[0].get() + 1)'''

if __name__ == "__main__":
    root = Tk()
    root.title("CaneCheck")
    root.minsize(800, 600)  
    root.geometry("1024x768")
    root.configure(bg="white")
    
    reports_page = DashboardPage(root)
    reports_page.pack(fill="both", expand=True)
    
    root.mainloop()
