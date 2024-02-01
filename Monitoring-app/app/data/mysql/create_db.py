import hashlib
from app.data.mysql.connection import Connection

class DatabaseService:
    def __init__(self, database_name="monitoring"):
        self.DATABASE_NAME = database_name
        self.db_service = Connection(database_name).connection
        self.init_database()

    def init_database(self) -> None:
        try:
            self.create_database()
            self.create_tables()
        except Exception as err:
            print(err)

    def create_database(self) -> None:
        cursor = self.db_service.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.DATABASE_NAME}")
        cursor.close()

    def create_tables(self) -> None:
        self.db_service.database = self.DATABASE_NAME
        cursor = self.db_service.cursor()

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
                FOREIGN KEY (device_id) REFERENCES devices(id),
                disk_size float
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS iotdevices (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                adresse_ip VARCHAR(50) NOT NULL,
                adresse_mac VARCHAR(50) NOT NULL,
                longitude VARCHAR(50) NOT NULL,
                latitude VARCHAR(50) NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS iot_information (
                id INT AUTO_INCREMENT PRIMARY KEY,
                temperature double,
                iot_id int,
                FOREIGN KEY (iot_id) REFERENCES iotdevices(id),
                time timestamp
            )
        ''')
        
        cursor.close()

    def hash_password(self, password: str) -> str:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    def insert_user(self, username: str, password: str) -> None:
        hashed_password = self.hash_password(password)
        cursor = self.db_service.cursor()
        cursor.execute("INSERT INTO users (username, passwd) VALUES (%s, %s)", (username, hashed_password))
        self.db_service.commit()
        cursor.close()

    def get_user_by_username_password(self, username: str, password: str) -> any:
        hashed_password = self.hash_password(password)
        cursor = self.db_service.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND passwd = %s", (username, hashed_password))
        user_data = cursor.fetchone()
        cursor.close()
        return user_data

if __name__ == "__main__":
    db_service = DatabaseService()
    # Perform any additional operations as needed
