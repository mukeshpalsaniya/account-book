import sqlite3


class DbConnect:
    def __init__(self):
        try:
            self.db = sqlite3.connect("./DB/first.db")
        except Exception as e:
            print(e)


