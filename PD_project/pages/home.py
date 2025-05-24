from tkinter import *
import tkinter as tk
from pathlib import Path
import RPi.GPIO as GPIO

#import cv2 
#from PIL import Image, ImageTk 
#from datetime import datetime


from stepper import Stepper
from pins import Pins
from camera import Camera
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)



PATH = Path(__file__).parent / 'assets'


class HomePage(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)        



        
        # Sidebar
        main_frame = tk.Frame(self, bg='#9E8DB9', width=50)
        main_frame.pack(padx=10, pady=10, fill=BOTH, expand=True)


        self.images = [
            tk.PhotoImage(name='logo', file=PATH / 'sugarcane.png'),
            tk.PhotoImage(name='dashboard', file=PATH / 'dashboard_icon.png'),
            tk.PhotoImage(name='reports', file=PATH / 'reports_icon.png'),
            tk.PhotoImage(name='help', file=PATH / 'help_icon.png')]

        self.logo_text = tk.Label(
            master=main_frame,
            text='CANECHECK',
            font=('Lexend', 20, 'bold'),
            bg='#9E8DB9',
            fg='white' ) # Adjust text color
    
        
        self.logo = tk.Label(
            master=main_frame,
            image=self.images[0],  
            bg='#9E8DB9',
            borderwidth=0 )

        self.disp = Label(self)

        self.logo_text.pack(fill=BOTH, expand=True)
        self.logo.pack(fill=BOTH, expand=True)
        self.disp.pack(fill=BOTH, expand=True)
        self.update()
        self.strtBtn = Button(main_frame, text = "Initialize", command= self.setup, height=5)
        self.strtBtn.pack(fill="x")        

    def setup(self):
        self.disp.config(text = "Initializing system")

        try:
            #Pins(varpin1, varpin2, varpin3, enable, start, conveyor, magnetic door, feeder)
            pins = Pins(25,8,7, 23,24, 14,15, 12)
            
            #camera setup
            cam = Camera(0)
            cam.start_camera()

            pins.all_pin_low()

            self.disp.config(text = "System Ready")

        except Exception as e:
            self.disp.config(text = f"Setup failed. Error {e}")





if __name__ == "__main__":
    root = Tk()
    root.title("Home Page")
    root.geometry("800x600")
    root.configure(bg="white")
    
    reports_page = HomePage(root)
    reports_page.pack(fill="both", expand=True)
    
    root.mainloop()
