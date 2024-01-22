from app.data.mysql.connection import Connection

class CreateDatabase :
    def __init__(self) -> None:
        self.DATABASE_NAME : str = "monitoring"
        self.connection =  Connection().connection
        self.init_database()

    def init_database(self) -> None :
        try :
            self.create_database()
            self.create_tables()
            self.connection.close()
        except Exception as err :
            print(err)

    def create_database(self) -> None :
        cursor = self.connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.DATABASE_NAME}")  
        cursor.close()  
            
    def create_tables(self) ->None :
        self.connection.database = self.DATABASE_NAME
        cursor = self.connection.cursor()

        # Creation of the users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                passwd VARCHAR(255) NOT NULL
            )
        ''')

       # Creation of the devices table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                id INT AUTO_INCREMENT PRIMARY KEY,
                device_name VARCHAR(255) NOT NULL,
                device_ip VARCHAR(50) NOT NULL,
                device_mac_address VARCHAR(50) NOT NULL
            )
        ''')

        # Creation of the device_information table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS device_informations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                memory_usage FLOAT NOT NULL,
                cpu_usage FLOAT NOT NULL,
                disk_space_used FLOAT NOT NULL,
                device_id INT,
                FOREIGN KEY (device_id) REFERENCES devices(id)
            )
        ''')

        cursor.close()
        

if __name__ == "__main__" :
    cr : CreateDatabase = CreateDatabase()
    