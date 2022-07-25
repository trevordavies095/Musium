import sqlite3


class DbLayer:
    conn = None

    def __init__(self):
        try:
            self.conn = sqlite3.connect("AlbumRatings.db")
        except Exception as e:
            print(e)

    
    