import os
import sqlite3


class DbConnect:
    def __init__(self):
        try:
            os.stat("./DB/first.db")
            self.db = sqlite3.connect("./DB/first.db")
        except Exception as e:
            self.db = sqlite3.connect("./DB/first1.db")
            print("Exception: using default DB")


