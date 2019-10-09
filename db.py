import sqlite3


class Trial:

    def __init__(self):
        self.conn = sqlite3.connect("DB.db")
        # self.conn = sqlite3.connect(":memory:")
        print("Opened database successfully")

    def maketable(self):
        command = "CREATE table TREES ( X string, Y string, X1 string, Y1 string, height string)"
        self.conn.execute(command)

    def makeinsert(self,tablename="",col1="",col2="", col3="", col4="", col5=""):
        command = "INSERT into "+tablename + " VALUES ("+str(col1)+","+str(col2)+", "+str(col3)+","+str(col4)+","+str(col5)+")"
        #print(command)
        return command

    def put_record(self,command=""):
        self.conn.execute(command)
        self.conn.commit()

    def read_record(self,query=""):
        data = self.conn.execute(query);
        for row in data:
            for col in row:
                print(col, end = " ")
            print()

    def make_query(self,tablename="",clause=""):
        aquery = "Select * from " + tablename + " where height >= " + clause
        return aquery

    def __del__(self):
        self.conn.close()
        print("Close the connection to DB")