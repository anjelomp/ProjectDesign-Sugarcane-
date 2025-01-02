from pathlib import Path
import tkinter as tk
from tkinter import ttk
import sqlite3
# Importing the DashboardPage, ReportsPage, and HelpPage classes
from dashboard import DashboardPage
from reports import ReportsPage
from helps import HelpPage
# from calibrate import CalibratePage

PATH = Path(__file__).parent / 'assets'


class CaneCheckMain(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill=tk.BOTH, expand=tk.YES)

        self.conn = sqlite3.connect('canecheck.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

        # Application images
        self.images = [
            tk.PhotoImage(name='logo', file=PATH / 'sugarcane.png'),
            tk.PhotoImage(name='dashboard', file=PATH / 'dashboard_icon.png').subsample(3, 3),
            tk.PhotoImage(name='reports', file=PATH / 'reports_icon.png').subsample(3, 3),
            tk.PhotoImage(name='help', file=PATH / 'help_icon.png').subsample(3, 3)
        ]

        # Header
        hdr_frame = tk.Frame(self, bg='#9E8DB9')
        hdr_frame.pack(fill=tk.X)

        hdr_label = tk.Label(
            master=hdr_frame,
            image=self.images[0],  # Assuming the logo is the header background
            bg='#9E8DB9',
            borderwidth=0
        )
        hdr_label.pack(side=tk.LEFT, padx=0, pady=10)

        logo_text = tk.Label(
            master=hdr_frame,
            text='CANECHECK',
            font=('Arial', 34, 'bold'),
            bg='#9E8DB9',
            fg='white'  # Adjust text color
        )
        logo_text.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5)

        # Sidebar
        sidebar_frame = tk.Frame(self, bg='dark gray', width=100)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Action buttons
        pages = ["Dashboard","Calibrate","Reports"]  # Page names
        self.pages = {}  # Dictionary to hold page instances

        for page_name in pages:
            button = tk.Button(
                master=sidebar_frame,
                image=self.images[pages.index(page_name) + 1],  # Get the corresponding image
                text=page_name,
                compound=tk.TOP,
                borderwidth=0,
                bg='dark gray',
                command=lambda page_name=page_name: self.show_page(page_name)
            )
            button.pack(fill=tk.X, padx=5, pady=5)

        # Create and add pages to the dictionary
        self.pages["Dashboard"] = DashboardPage(self)
        # self.pages["Calibrate"] = CalibratePage(self)
        self.pages["Reports"] = ReportsPage(self)
        

        # Show the initial page
        self.show_page("Dashboard")

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Session (
                                Session_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                SessionName TEXT,
                                StartTime TEXT,
                                EndTime TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS SessionDetail (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                Session_ID INTEGER,
                                Sequence INTEGER,
                                FileName TEXT,
                                Variety_ID TEXT,
                                ImageData TEXT,
                                FOREIGN KEY(Session_ID) REFERENCES Session(Session_ID))''')
        self.conn.commit()
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
