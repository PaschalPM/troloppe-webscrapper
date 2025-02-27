import sqlite3

class Db():
    conn = None
    
    def __init__(self):
        self.conn = sqlite3.connect('storage/db.sqlite')
        
    def get_cursor(self):
        return self.cursor