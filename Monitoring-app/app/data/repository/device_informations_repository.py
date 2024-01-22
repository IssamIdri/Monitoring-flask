from app.data.mysql.connection import Connection

class DeviceInforamtionsRepository :
    def insert_device_info(self, memory_usage : str, cpu_usage : str, disk_space_used : str, disk_size : str, device_id : str) -> None:
        connection = Connection("monitoring").connection
        cursor = connection.cursor()
        cursor.execute(
            '''INSERT INTO device_informations (memory_usage, cpu_usage, disk_space_used, disk_size,device_id)
            VALUES (%s, %s, %s, %s, %s)''', (memory_usage, cpu_usage, disk_space_used,disk_size, device_id))
        connection.commit()
        cursor.close()
        connection.close()
    
    def get_device_inforamtions_by_device_id(self, device_id : str) -> list:
        connection = Connection("monitoring").connection
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM device_informations where device_id LIKE %s',(device_id,))
        result : list = cursor.fetchall()
        cursor.close()
        connection.close()
        return result



if __name__ == "__main__" :
    pass