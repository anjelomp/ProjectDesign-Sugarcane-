from pathlib import Path
import tkinter as tk
from tkinter import ttk

# Importing the DashboardPage, ReportsPage, and HelpPage classes
from frontEnd import DashboardPage
from reports import ReportsPage
from helps import HelpPage
#from calibrate import CalibratePage
#from setup import SetupPage

PATH = Path(__file__).parent / 'assets'


class CaneCheckMain(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill=tk.BOTH, expand=tk.YES)
  
        
        # Logos
        self.images = [
            tk.PhotoImage(name='logo', file=PATH / 'sugarcane.png'),
            tk.PhotoImage(name='dashboard', file=PATH / 'dashboard_icon.png'),
            tk.PhotoImage(name='reports', file=PATH / 'reports_icon.png'),
            tk.PhotoImage(name='help', file=PATH / 'help_icon.png')
        ]
        # Sidebar
        sidebar_frame = tk.Frame(self, bg='#9E8DB9', width=200)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
	
        logo_text = tk.Label(
            master=sidebar_frame,
            text='CANECHECK',
            font=('Lexend', 14, 'bold'),
            bg='#9E8DB9',
            fg='white'  # Adjust text color
        )
        
        
        self.images[0]= self.images[0].subsample(2)
        
        logo = tk.Label(
            master=sidebar_frame,
            image=self.images[0],  
            bg='#9E8DB9',
            borderwidth=0 
        )

        logo.grid(row = 0, column = 0, pady = 15)
        logo_text.grid(row = 0, column = 1,  padx=5, pady=15)

                
        # Action buttons
        pages = ["Dashboard","Reports"]  # Page names
        self.pages = {}  # Dictionary to hold page instances

        rownum = 1
        for page_name in pages:
            self.images[pages.index(page_name) + 1]=self.images[pages.index(page_name) + 1].subsample(4)

            logo_button = tk.Button(
                master=sidebar_frame,
                image=self.images[pages.index(page_name) + 1],  # Get the corresponding image
                compound=tk.TOP,
                borderwidth=0,
                bg='#9E8DB9',
                highlightthickness = 0, bd = 0,
                command=lambda page_name=page_name: self.show_page(page_name)
            )

            text_button = tk.Button(
                master=sidebar_frame,
                text=page_name,
                font=('Arial', 14),
                bg='#9E8DB9',
                fg='white',  # Adjust text color
                highlightthickness = 0, bd = 0,
                command=lambda page_name=page_name: self.show_page(page_name)
                
                 )
            text_button.grid(row = rownum, column = 1, pady = 2, sticky ='w')
            logo_button.grid(row=rownum, column = 0, pady = 2)
            rownum +=1
            
        # Create and add pages to the dictionary
        self.pages["Dashboard"] = DashboardPage(self)
        self.pages["Reports"] = ReportsPage(self)
        

        # Show the initial page
        self.show_page("Dashboard")

    def show_page(self, page_name):
        # Hide all pages
        for page in self.pages.values():
            page.pack_forget()

        # Show the selected page
        self.pages[page_name].pack(fill=tk.BOTH, expand=True)


if __name__ == '__main__':
    app = tk.Tk()
    app.title("CaneCheck: Sugarcane Variety Detection")
    app.geometry("800x480")  # Set initial window size
    app.grid_rowconfigure(0, weight=1)  # Make the rows expand
    app.grid_rowconfigure(1, weight=1)
    app.grid_columnconfigure(0, weight=1)  # Center the column
    CaneCheckMain(app)
    app.mainloop()
