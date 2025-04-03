
import sqlite3


class DbPage:
 
    def setup(self):
        self.conn = sqlite3.connect('db1.db')
        self.cursor = self.conn.cursor()
        
        #session table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Session (
                                Session_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                SessionName TEXT,
                                StartTime TEXT,
                                EndTime TEXT)''')
        #detection table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS SessionDetail (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                Session_ID INTEGER,
                                Sequence INTEGER,
                                FileName TEXT,
                                Variety_ID TEXT,
                                ImageData TEXT,
                                FOREIGN KEY(Session_ID) REFERENCES Session(Session_ID))''')
        #variety table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS images (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                image_name TEXT NOT NULL,
                                variety INTEGER NOT NULL,
                                timestamp TEXT NOT NULL)''')
        self.conn.commit()


