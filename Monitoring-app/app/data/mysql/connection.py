import mysql.connector

class Connection:
    def __init__(self, dattabase_name : str="")->None:
        self.connection= self.get_connection(dattabase_name)
    def get_connection(self ,database_name=""):
        try :
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database=database_name
            )
        except Exception as err:
            print(err)
            return None
        
if __name__=="__main__" :
    con :Connection =Connection()
    print(con.connection)