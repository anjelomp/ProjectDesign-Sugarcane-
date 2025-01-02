from tkinter import *
from tkinter import ttk
import sqlite3

class ReportsPage(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        # Initialize SQLite database
        self.db_connection = sqlite3.connect("reports.db")
        self.cursor = self.db_connection.cursor()
        self.setup_database()

        # Search Frame
        search_frame = Frame(self, bg="lightgrey")
        search_frame.pack(pady=20)

        # Search Entry
        self.search_entry = Entry(search_frame, width=50, font=("Arial", 16))
        self.search_entry.grid(row=0, column=0, padx=10, pady=10)

        # Search Button
        search_button = Button(
            search_frame, 
            text="Search", 
            command=self.perform_search, 
            bg="#9E8DB9", 
            fg="white", 
            font=("Arial", 14), 
            relief=RAISED
        )
        search_button.grid(row=0, column=1, padx=10, pady=10)

        # Creating the table
        self.table = ttk.Treeview(self, columns=("Name", "Date"), show="headings", height=10)
        self.table.heading("Name", text="Name")
        self.table.heading("Date", text="Date")

        # Style for the table
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="lightgrey")
        style.map("Treeview", background=[("selected", "lightblue")])

        self.table.pack(pady=20, fill="both", expand=True)

        # Bind selection event
        self.table.bind("<<TreeviewSelect>>", self.handle_row_selection)

        # Load initial data from the database
        self.load_data_from_db()

        # Action Frame for buttons
        self.action_frame = Frame(self, bg="white")
        self.action_frame.pack(pady=10)

        self.view_details_button = Button(
            self.action_frame, 
            text="View Details", 
            command=self.view_details, 
            state=DISABLED, 
            font=("Arial", 14), 
            bg="blue", 
            fg="white"
        )
        self.view_details_button.pack(pady=5)

        # Variable to store selected row's item ID
        self.selected_item_id = None

    def setup_database(self):
        # Create table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                variety TEXT NOT NULL,
                image BLOB
            )
        """)

        # Insert sample data if the table is empty
        self.cursor.execute("SELECT COUNT(*) FROM reports")
        if self.cursor.fetchone()[0] == 0:
            sample_data = [
                ("John", "2024-03-04", "Variety A", None),
                ("Alice", "2024-03-05", "Variety B", None),
                ("Bob", "2024-03-06", "Variety C", None),
                ("Charlie", "2024-03-07", "Variety D", None),
                ("Diana", "2024-03-08", "Variety E", None)
            ]
            self.cursor.executemany("INSERT INTO reports (name, date, variety, image) VALUES (?, ?, ?, ?)", sample_data)
            self.db_connection.commit()

    def load_data_from_db(self):
        # Clear existing data in the table
        for row in self.table.get_children():
            self.table.delete(row)

        # Fetch data from the database
        self.cursor.execute("SELECT id, name, date FROM reports")
        rows = self.cursor.fetchall()

        # Insert data into the table
        for row in rows:
            item_id = row[0]
            self.table.insert("", "end", values=(row[1], row[2]), tags=(str(item_id),))

    def handle_row_selection(self, event):
        selected_item = self.table.selection()
        if selected_item:
            item_tags = self.table.item(selected_item[0], "tags")
            if item_tags:
                self.selected_item_id = int(item_tags[0])
                self.view_details_button.config(state=NORMAL)
        else:
            self.selected_item_id = None
            self.view_details_button.config(state=DISABLED)

    def view_details(self):
        if self.selected_item_id is None:
            return

        # Fetch the details of the selected item from the database
        self.cursor.execute("SELECT name, date, variety, image FROM reports WHERE id = ?", (self.selected_item_id,))
        details = self.cursor.fetchone()

        if details:
            # Create a new Toplevel window to display the details
            details_window = Toplevel(self)
            details_window.title("Report Details")
            details_window.geometry("400x300")
            details_window.configure(bg="white")

            Label(details_window, text="--- Report Details ---", font=("Arial", 16, "bold"), fg="blue", bg="white").pack(pady=10)

            frame = Frame(details_window, padx=20, pady=10, bg="white")
            frame.pack(fill="both", expand=True)

            Label(frame, text="Name:", font=("Arial", 14), anchor="w", bg="white").grid(row=0, column=0, sticky="w", pady=5)
            Label(frame, text=details[0], font=("Arial", 12), bg="white").grid(row=0, column=1, sticky="w", pady=5)

            Label(frame, text="Date:", font=("Arial", 14), anchor="w", bg="white").grid(row=1, column=0, sticky="w", pady=5)
            Label(frame, text=details[1], font=("Arial", 12), bg="white").grid(row=1, column=1, sticky="w", pady=5)

            Label(frame, text="Variety:", font=("Arial", 14), anchor="w", bg="white").grid(row=2, column=0, sticky="w", pady=5)
            Label(frame, text=details[2], font=("Arial", 12), bg="white").grid(row=2, column=1, sticky="w", pady=5)

            Label(frame, text="Image:", font=("Arial", 14), anchor="w", bg="white").grid(row=3, column=0, sticky="w", pady=5)
            image_label = Label(frame, text="[Placeholder Image]", font=("Arial", 12), bg="lightgrey", width=20, height=5)
            image_label.grid(row=3, column=1, sticky="w", pady=5)

            Button(details_window, text="Close", command=details_window.destroy, font=("Arial", 12), bg="red", fg="white").pack(pady=20)

    def perform_search(self):
        search_query = self.search_entry.get().strip()
        
        # Clear existing data in the table
        for row in self.table.get_children():
            self.table.delete(row)

        # Search the database
        query = "SELECT id, name, date FROM reports WHERE name LIKE ?"
        self.cursor.execute(query, (f"%{search_query}%",))
        rows = self.cursor.fetchall()

        # Insert search results into the table
        for row in rows:
            item_id = row[0]
            self.table.insert("", "end", values=(row[1], row[2]), tags=(str(item_id),))

    def exit_app(self):
        # Close the database connection and exit the app
        self.db_connection.close()
        self.master.destroy()

if __name__ == "__main__":
    root = Tk()
    root.title("Reports Page")
    root.geometry("800x600")
    root.configure(bg="white")

    reports_page = ReportsPage(root)
    reports_page.pack(fill="both", expand=True)

    root.protocol("WM_DELETE_WINDOW", reports_page.exit_app)
    root.mainloop()
