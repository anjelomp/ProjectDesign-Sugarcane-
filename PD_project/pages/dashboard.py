from tkinter import *
import cv2 
from PIL import Image, ImageTk 
import os
from datetime import datetime
import threading
import array
import time
import RPi.GPIO as GPIO

from stepper import Stepper
from gpiozero import DistanceSensor
from pins import Pins
from camera import Camera
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)




class DashboardPage(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        
        self.initial()


    def initial(self):

        self.output = Label(self, 
            font=("Helvetica", 16, "bold"),  # Font family, size, and style
            state=DISABLED)
        self.output.pack(pady=30)  

        self.start_button = Button(self, 
            text="Start",
            font=("Helvetica", 16, "bold"),  # Font family, size, and style
            width=20,  # Number of text characters wide
            height=2,  # Number of text lines tall
            command=self.start_setup)
        self.start_button.pack(pady=30)  

        self.bind('<Escape>', lambda e: self.master.destroy()) 


    def start_setup(self):

        self.start_button.pack_forget()
                
        #setup
        try:

            #counters counter[0]--> caneCount [6]--> waitCount
            self.counter = array.array('i',[0,0,0,0,0,0,0])

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


            self.output.config(text="\n\nSetup Complete. Proceed?\n")
            self.output.config(state=NORMAL)
            self.yes_button = Button(self, text="Yes", 
                font=("Helvetica", 16, "bold"),  # Font family, size, and style
                width=20,  # Number of text characters wide
                height=2,  # Number of text lines tall
                command=self.start_process)
            self.yes_button.pack( side="left", padx=10) 
            self.back_button = Button(self, text="Back", 
                font=("Helvetica", 16, "bold"),  # Font family, size, and style
                width=20,  # Number of text characters wide
                height=2,  # Number of text lines tall
                command=self.reload)
            self.back_button.pack( side="left", padx=10) 
 

        except Exception as e:
            
            self.output.config(text=f"Setup failed. Error {e}")
            self.output.config(state=NORMAL)
            self.back_button = Button(self, text="Back", 
                font=("Helvetica", 16, "bold"),  # Font family, size, and style
                width=20,  # Number of text characters wide
                height=2,  # Number of text lines tall
                command=self.reload)
            self.back_button.pack(pady=30) 

    def reload(self):
         self.yes_button.pack_forget()
         self.back_button.pack_forget()
         self.output.pack_forget()
         self.initial()


    def start_process(self):
        self.yes_button.pack_forget()
        self.back_button.pack_forget()
        self.output.pack_forget()

        self.start_label  = Label(self, text="start:0", height = 5)
        self.enable_label = Label(self,  text="enable:0",height = 5)
        self.var_label    = Label(self,  text="var:no detected",height = 5)
        self.relay_stat = Label(self,  text="relay:disabled",height = 5)
        self.stepper_stat = Label(self,  text="conveyor:disabled",height = 5)
        self.son_det  = Label(self,  text="sensor:no detected",height = 5)
        self.disp = Label(self)
        
        self.start_label.grid(  row=0, column=0,padx=5)
        self.enable_label.grid( row=0, column=1,padx=5)
        self.var_label.grid(    row=0, column=2,padx=5)
        self.relay_stat.grid(   row=0, column=3,padx=5)
        self.stepper_stat.grid( row=1, column=0,padx=5)
        self.son_det.grid(      row=1, column=1,padx=5)
        self.disp.grid(      row=2, column=0,padx=5)
        self.update()        


        try:
            self.var = 1 #temp
	    #start 1
            self.pins.start_high()
            self.start_label.config(text="start:1")
            self.update()            
	    
	    #conveyor start
            self.thread = threading.Thread(target=self.stepper.run, daemon=True)
            self.thread.start()
            self.stepper.ena_low()
            self.stepper_stat.config(text="conveyor:engaged", state=NORMAL)
            self.update()            
            
            #relay 
            self.relay_stat.config(text="relay:engaged", state=NORMAL)
            self.update()            
            self.pins.relay_activate()
            self.relay_stat.config(text="relay:disabled", state=NORMAL)
            self.update()            

            while True:
                

                #detect cane within range of camera
                dist = self.ultrasonic.distance 
                if dist < 1.0:
                    self.son_det.config(text="sensor: " + str(dist), state=NORMAL)
                    self.update()            
                    
                    #cane count
                    self.counter[0]+=1 
                    
                    #capture
                    name= str(self.counter[0])+"_cane.jpg"
                    self.cam.capture_image("images/"+name)
                    image = Image.open("images/"+name)
                    image = image.resize((100,100))
                    photo = ImageTk.PhotoImage(image)
                    self.disp.grid_forget()
                    self.update()
                    
                    self.disp.config(image=photo)
                    self.disp.grid(row=2, column=0,padx=5)
                    self.update()
                    

                    #enaPin disable
                    self.pins.enable_low()
                    self.enable_label.config(text="enable:0")                    
                    self.pins.reset_varPins()
                    self.update()

                    #temp ML var detection
                    if self.var == 5:
                            self.var = 1
                    else:
                            self.var += 1
                
                    #varPins activate, increment varCount
                    self.counter[self.var]+=1
                    self.pins.out_to_pins(self.var)
                    self.var_label.config(text="variety: "+str(self.var))
                    self.update()                    

                    #enaPin enable
                    self.pins.enable_high()
                    self.enable_label.config(text="enable:1")
                    self.update()
                    
                    self.disp.grid_forget()
                    self.update()
                    
                    self.disp.config(text="cane #"+str(self.counter[0])+" Variety:"+str(self.var)+
                            "\nVariety 1:"+str(self.counter[1])+
                            "\nVariety 2:"+str(self.counter[2])+
                            "\nVariety 3:"+str(self.counter[3])+
                            "\nVariety 4:"+str(self.counter[4])+
                            "\nVariety 5:"+str(self.counter[5]))
                    
                    self.disp.grid(row=2, column=0,padx=5, pady=5)
                    self.update()

                    self.relay.config(text="relay:engaged")
                    self.update()
                    self.pins.relay_activate()
                    self.relay.config(text="relay:disabled")
                    self.update()
                    
                    self.counter[6] = 0
                else:
                    self.counter[6] += 1 #wait counter
                    if self.counter[6]==5:
                    
                            self.relay_stat.config(text="relay:engaged")
                            self.update()
                            self.pins.relay_activate()
                            self.relay_stat.config(text="relay:disabled")
                            self.update()
      
                    self.disp.config(text="Ultrasonic not in range. Count: "+str(self.counter[6]))
                    self.update()            

                    self.after(3000)
                
                if self.counter[6] >= 10:
                    self.pins.start_low()
                    self.start_label.config(text="start:0")

                    self.disp.grid_forget()
                    self.update()                    
                    self.disp.config(text="No Cane Detected.\nSUMMARY\nTotal Cane: "+str(self.counter[0])+
                            "\nVariety 1:"+str(self.counter[1])+
                            "\nVariety 2:"+str(self.counter[2])+
                            "\nVariety 3:"+str(self.counter[3])+
                            "\nVariety 4:"+str(self.counter[4])+
                            "\nVariety 5:"+str(self.counter[5])+
                            "Process End")
                    self.disp.grid(row=2, column=0,padx=5, pady=5)
                    self.update()

                    break 

            # Release the webcam
            self.cam.release()
            self.stepper.ena_high()
            self.stepper_stat.config(text="conveyor:disabled")
 

        except Exception as e:
            self.disp.config(text=f"Error {e}")




if __name__ == "__main__":
    root = Tk()
    root.title("Dashboard Page")
    root.geometry("800x600")
    root.configure(bg="white")
    
    reports_page = DashboardPage(root)
    reports_page.pack(fill="both", expand=True)
    
    root.mainloop()
