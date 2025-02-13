<<<<<<< Updated upstream
from tkinter import *
import cv2 
from PIL import Image, ImageTk 
import os
from datetime import datetime
import threading

class DashboardPage(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self.vid = cv2.VideoCapture(0) 
        self.width, self.height = 800, 600
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, self.width) 
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height) 

        # Create a label for the camera preview
        self.label_widget = Label(self, borderwidth=5, relief="ridge")
        self.label_widget.grid(row=1, column=0, padx=10, pady=10)  

        self.capture_image = False
        self.image_count = 0
        self.capture_start_time = None

        # Create a label to display the image count
        self.count_label = Label(self, text="Images captured: 0")
        self.count_label.grid(row=1, column=1, padx=10, pady=10)  

        # Create a button to capture an image
        self.capture_button = Button(self, text="Capture Image", command=self.toggle_capture)
        self.capture_button.grid(row=3, column=0, padx=10, pady=10)  

        # Create a button to stop capturing
        self.stop_button = Button(self, text="Stop Capture", command=self.stop_capture, state=DISABLED)
        self.stop_button.grid(row=4, column=0, padx=10, pady=10)  

        self.bind('<Escape>', lambda e: self.master.destroy()) 

        # Start the camera preview thread
        self.camera_thread = threading.Thread(target=self.open_camera)
        self.camera_thread.daemon = True
        self.camera_thread.start()

    def open_camera(self): 
        while True:
            ret, frame = self.vid.read()  # Capture the video frame by frame
            if ret:  # Check if the frame is valid
                opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
                captured_image = Image.fromarray(opencv_image)  
                photo_image = ImageTk.PhotoImage(image=captured_image) 
                self.label_widget.photo_image = photo_image 
                self.label_widget.configure(image=photo_image) 
                self.label_widget.image = photo_image  # Keep a reference to prevent garbage collection

    def toggle_capture(self):
        if not self.capture_image:
            self.capture_button.config(text="Capturing...")
            self.stop_button.config(state=NORMAL)
            self.capture_image = True
            self.capture_start_time = datetime.now()  # Set the start time
            self.capture_images_continuously()
        else:
            self.capture_button.config(text="Capture Image")
            self.stop_button.config(state=DISABLED)
            self.capture_image = False

    def capture_images_continuously(self):
        if self.capture_image:
            current_time = datetime.now()
            time_difference = current_time - self.capture_start_time
            if time_difference.total_seconds() >= 5:  # Check if 5 seconds have passed
                self.capture_start_time = current_time  # Update the start time
                self.capture_image_func()  # Capture an image
            self.master.after(10, self.capture_images_continuously)  # Continue capturing images

    def capture_image_func(self):
        ret, frame = self.vid.read()
        if ret:
            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
            captured_image = Image.fromarray(opencv_image) 
            self.save_image(captured_image)
            self.image_count += 1
            self.count_label.config(text=f"Images captured: {self.image_count}")

    def stop_capture(self):
        self.capture_button.config(text="Capture Image")
        self.stop_button.config(state=DISABLED)
        self.capture_image = False

    def save_image(self, image):
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        session_path = os.path.join("captured_images")
        if not os.path.exists(session_path):
            os.makedirs(session_path)
        image.save(os.path.join(session_path, f"sugarcane_image_{timestamp}.png"))

    def exit_app(self):
        self.vid.release()  # Release the camera
        self.master.destroy()

if __name__ == "__main__":
    root = Tk()
    root.title("Dashboard Page")
    root.geometry("800x600")
    root.configure(bg="white")
    
    reports_page = DashboardPage(root)
    reports_page.pack(fill="both", expand=True)
    
    root.mainloop()
=======
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
    

    def update_disp(self):
        
        self.disp = Label(self)

        image = Image.open("images/sample.jpg")
        image = image.resize((200,200))
        photo = ImageTk.PhotoImage(image)  
        self.img_disp = Label(self,image=photo)

        
        #live count
        self.livec_label = Label(self, 
                                 text = "Live Count",
                                 font = ("Lexend", 14, "bold"))        
        self.livec = Label(self, textvariable = self.counter[0])
        
        #sensor
        self.sensor_label = Label(self,
                                  text = "Sensor",
                                  font = ("Lexend", 14, "bold"))
        self.sensor_disp = Label(self, textvariable = self.sensor)
        
        #variety detected
        self.var_label = Label(self,
                               text = "Variety Detected",
                               font = ("Lexend", 14, "bold"))
        self.var_disp = Label(self, textvariable = self.vard)
        
        #conveyor actuator enable
        self.conv_disp = Label(self, text = "conv:"+str(self.conv))
        self.act_disp = Label(self, text = "actuator:"+str(self.act))
        self.ena_disp = Label(self, text = "enable:"+str(self.enable))        

        #variety counter
        self.varcount1_label = Label(self,
                                    text = "Variety 1",
                                    font = ("Lexend", 14, "bold"))        
        self.varcount2_label = Label(self,
                                    text = "Variety 2",
                                    font = ("Lexend", 14, "bold"))
        self.varcount3_label = Label(self,
                                    text = "Variety 3",
                                    font = ("Lexend", 14, "bold"))
        self.varcount4_label = Label(self,
                                    text = "Variety 4",
                                    font = ("Lexend", 14, "bold"))
        self.varcount5_label = Label(self,
                                    text = "Variety 5",
                                    font = ("Lexend", 14, "bold"))

        self.varcount1_disp = Label(self, textvariable = self.counter[1])
        self.varcount2_disp = Label(self, textvariable = self.counter[2])
        self.varcount3_disp = Label(self, textvariable = self.counter[3])
        self.varcount4_disp = Label(self, textvariable = self.counter[4])
        self.varcount5_disp = Label(self, textvariable = self.counter[5])
                                    


                
        self.img_disp.grid(    row=0, column=0, columnspan = 3, rowspan=5)
        self.livec_label.grid( row=0, column=4, columnspan = 2)
        self.livec.grid(       row=1, column=4, columnspan = 2)
        self.sensor_label.grid(row=2, column=4, columnspan = 2)
        self.sensor_disp.grid( row=3, column=4, columnspan = 2)
        self.var_label.grid(   row=4, column=4, columnspan = 2)
        self.var_disp.grid(    row=5, column=4, columnspan = 2)
        self.conv_disp.grid(   row=6, column=4, columnspan = 2)
        self.act_disp.grid(    row=7, column=4, columnspan = 2)
        self.ena_disp.grid(    row=8, column=4, columnspan = 2)
        self.disp.grid(        row=5, column=0, columnspan = 3, rowspan = 4)
        
        self.varcount1_label.grid(row=9, column=0)
        self.varcount2_label.grid(row=9, column=1)
        self.varcount3_label.grid(row=9, column=2)
        self.varcount4_label.grid(row=9, column=3)
        self.varcount5_label.grid(row=9, column=4)
        
        self.varcount1_disp.grid(row=10, column=0)
        self.varcount2_disp.grid(row=10, column=1)
        self.varcount3_disp.grid(row=10, column=2)
        self.varcount4_disp.grid(row=10, column=3)
        self.varcount5_disp.grid(row=10, column=4)
                
        self.update()        


    def initial_var(self):
        self.counter = array.array('i',[0,0,0,0,0,0,0])
        self.start = 0
        self.enable = 0
        self.vard = None
        self.sensor = None
        self.act = 0
        self.conv = 0
    
    
    def start_process(self):
        self.yes_button.pack_forget()
        self.back_button.pack_forget()
        self.output.pack_forget()
        
        self.start = 0
        self.enable = 0
        self.vard = None
        self.sensor = None
        self.act = 0
        self.conv = 0





        try:
            self.var = 1 #temp
	        #start 1
            self.pins.start_high()
            self.pins.enable_low()
            self.start = 1
            self.enable = 0
            self.update_disp()            
	    
	        #conveyor start
            self.thread = threading.Thread(target=self.stepper.run, daemon=True)
            self.thread.start()
            self.stepper.ena_low()
            self.conv = 1
            self.update_disp()            
            
            #relay 
            self.act = 1
            self.update_disp()            
            self.pins.relay_activate()
            self.act = 0
            self.update_disp()            

            while True:
                

                #detect cane within range of camera
                dist = self.ultrasonic.distance 
                if dist < 1.0:
                    self.sensor = round(dist,2)
                    self.update_disp()            
                    
                    #cane count
                    self.counter[0]+=1 
                    self.update_disp()
                    
                    #capture
                    name= str(self.counter[0])+"_cane.jpg"
                    self.cam.capture_image("images/"+name)
                    image = Image.open("images/"+name)
                    image = image.resize((200,200))
                    photo = ImageTk.PhotoImage(image)
                    self.img_disp.grid_forget()
                    self.update()
                    
                    self.img_disp.config(image=photo)
                    self.img_disp.grid(row=3, column=0)
                    self.update()
                    

                    #enaPin disable
                    self.pins.enable_low()
                    self.enable = 0
                    self.update_disp()
                    
                    self.pins.reset_varPins()
                    self.vard = None
                    self.update_disp()

                    #temp ML var detection
                    if self.var == 5:
                            self.var = 1
                    else:
                            self.var += 1
                
                    #varPins activate, increment varCount
                    self.counter[self.var]+=1
                    self.pins.out_to_pins(self.var)
                    self.vard = self.var
                    self.update_disp()                    

                    #enaPin enable
                    self.pins.enable_high()
                    self.enable =1
                    self.update_disp()
                    
                    
                    self.act= 1
                    self.update_disp()
                    self.pins.relay_activate()
                    self.act=0
                    self.update_disp()
                    
                    self.counter[6] = 0
                    dist = None
                    self.sensor = None
                    self.update_disp()
                else:
                    self.counter[6] += 1 #wait counter
                    if self.counter[6]==5:
                            
                            self.act =1
                            self.update_disp()
                            self.pins.relay_activate()
                            self.act = 0
                            self.update_disp()
      
                    self.disp.grid_forget()
                    self.disp.config(text="Ultrasonic not in range. Count: "+str(self.counter[6]))
                    self.disp.grid(row=2, column=0)

                    self.update()            

                    self.after(1000)
                
                if self.counter[6] >= 10:
                    self.pins.start_low()
                    self.start = 0
       
                    self.disp.grid_forget()
                    self.update()
                    self.update_disp()                    
                    
                    self.disp.config(text="No Cane Detected. Process End")
                    self.disp.grid(row=2, column=0)
                    self.update()

                    break 

            # Release the webcam
            self.cam.release()
            self.stepper.ena_high()
            self.conv = 0
            self.update_disp() 

        except Exception as e:
            self.disp.grid_forget()
            self.update()
            
            self.disp.config(text=f"Error {e}")
            self.disp.grid(row=2, column=0)

            



if __name__ == "__main__":
    root = Tk()
    root.title("Dashboard Page")
    root.geometry("800x600")
    root.configure(bg="white")
    
    reports_page = DashboardPage(root)
    reports_page.pack(fill="both", expand=True)
    
    root.mainloop()
>>>>>>> Stashed changes
