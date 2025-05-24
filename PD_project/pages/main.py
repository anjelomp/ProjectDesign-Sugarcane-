import sqlite3
import datetime
import threading
import tkinter as tk
import random

from tkinter import Frame, Tk
from camera import Camera
from pins import Pins
from queues import Varqueue
from stepper import Stepper
from stepact import StepAct
from db import DbPage
from ml import MachineLearning

queue = []

class DashboardPage(Frame):


    def start(self,counter_vars,status_vars):
        self.counter_vars = counter_vars
        self.status_vars = status_vars
        
        try:
            # Initialize hardware and components

            #Pins(varpin1, varpin2, varpin3, enable, start, conveyor, magnetic door, feeder)

            self.pins = Pins(25,8,7, 23,24, 14,15, 12)
            self.pins.all_pin_low()

            #camera setup
            self.cam = Camera(0)
            self.cam.start_camera()
            
            # Initialize ML
            #self.ml = MachineLearning()
            #self.ml.setup()

            #Timeout
            self.timeout = 0
            
            #queue
            self.queues = Varqueue()
            
            # Start a new session in the DB
            self.db = DbPage()
            self.db.setup()
            self.detections = [] # data buffer storage
            start_time = datetime.datetime.now().isoformat()
            self.db.cursor.execute("INSERT INTO Session (SessionName, StartTime) VALUES (?, ?)",
                                   ("Session A", start_time))
            self.db.conn.commit()
            self.session_id = self.db.cursor.lastrowid  # Get the session id for linking detections
            self.sequence = 0  # To track order within this session


        except Exception as e:
            self.after(0,self.status_vars['prompt'].set(f"Error during setup: {e}"))
            return
        

        #run detection
        self.run_detection_loop()

    def run_detection_loop(self):
        try:
            #temp-for testing
            self.var = 1
            self.test = [1,2,1,3]
            self.index = 0

            #arduino com
            self.pins.start_high()
            self.pins.feeder_start()

            thread = threading.Thread(target=self.queues.loop, daemon=True)
            thread.start()



            self.status('system',"Scanning")            
            self.status('conveyor',"Running")
            self.status('actuator',"Feeding")


            while self.timeout <= 2000000:
                
                
                if not self.pins.readIR():
                    # Increment total cane counter
                    self.counter_vars[0].set(self.counter_vars[0].get() + 1)


                    # Build image filename
                    current_count = self.counter_vars[0].get()
                    self.imgname = f"{current_count}_cane.jpg"

                    # Capture image
                    self.cam.capture_image("images/" + self.imgname)
                    #self.update_var_pins()
                    
                    # Run ML detection (returns a variety as an integer, e.g., 1 to 5)
                    #self.var = self.ml.predict("images/" + self.imgname)
                    #self.var = random.randint(1,5)
                    self.var = self.test[self.index]
                    if self.index == 3:
                        self.index = 0
                    else:
                        self.index += 1

                    
                    # Update variety counter
                    self.counter_vars[self.var].set(self.counter_vars[self.var].get() + 1)
                    
                    #add to queue
                    
                    self.queues.add(self.var)
                                                                

                    #update display
                    self.status('img',self.imgname)
                    self.status('variety',str(self.var))
                    
                    # Buffer the detection event instead of immediate DB insertion
                    self.sequence += 1
                    detection_time = datetime.datetime.now().isoformat()
                    detection_record = (self.session_id, self.sequence, detection_time, "images/" + self.imgname, self.var)
                    self.detections.append(detection_record)

                    # Reset timeout indicator for this cycle
                    self.timeout = 0
                    while not self.pins.readIR():
                        pass
                    self.after(1000)
                else:
                    delay = 500  
                    self.after(delay)
                    self.timeout += delay
                    #self.update_var_pins()

            #end threading
            self.cam.release()
            self.stepact.start(False)
            self.stepact.act_extend()
            self.stepact.ena_high()

            self.status('system',"No Cane Detected")            
            self.status('conveyor',"Stopped")
            self.status('actuator',"Stopped")            


            # End of session: batch insert buffered detection events
            if self.detections:
                sql = """
                    INSERT INTO Detection (session_id, sequence, detection_time, image_file, variety_id)
                    VALUES (?, ?, ?, ?, ?)
                """
                self.db.cursor.executemany(sql, self.detections)
                self.db.conn.commit()

            # Update session end time
            end_time = datetime.datetime.now().isoformat()
            self.db.cursor.execute("UPDATE Session SET EndTime = ? WHERE session_id = ?",
                                   (end_time, self.session_id))
            self.db.conn.commit()

            
        except Exception as e:
            self.status_vars['prompt'].set(f"Error during detection: {e}")

 
    def status(self,var,value):
        self.status_vars[var].set(value)

    def signal_arduino(self):
        if self.ena_flag:
            self.pins.enable_high()
            self.ena_flag = False
        else:
            self.pins.enable_low()
            self.ena_flag = True


if __name__ == "__main__":
    root = Tk()
    root.title("CaneCheck")
    root.minsize(800, 600)
    root.geometry("1024x768")
    root.configure(bg="white")

    dashboard = DashboardPage(root)
    dashboard.pack(fill="both", expand=True)

    root.mainloop()


    '''
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
            self.counter_vars[0].set(self.counter_vars[0].get() + 1)'''
    



