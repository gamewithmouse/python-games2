import sqlite3



class DataBase:
    def __init__(self):
        self.db = sqlite3.connect("server.db")
        self.cursor = self.db.cursor()
    def adddata(self, table, columns, datas):
        columnstring = ",".join(columns)
        datastring = ",".join(datas)

        sql = "INSERT INTO "
        

