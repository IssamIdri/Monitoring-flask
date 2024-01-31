from app.data.mysql.connection import Connection
from datetime import datetime

class iot_DeviceInforamtionsRepository :
    def insert_iot_device_info(self, temperature:float,iot_device_id:str,time:datetime) -> None:
        connection = Connection("monitoring").connection
        cursor = connection.cursor()
        cursor.execute(
            '''INSERT INTO iot_information (temperature,iot_id,time)
            VALUES (%s,%s,%s)''', (temperature,iot_device_id,time))
        connection.commit()
        cursor.close()
        connection.close()
    
    def get_iot_device_inforamtions_by_device_id(self, id : str) -> list:
        connection = Connection("monitoring").connection
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM iot_information where iot_id = %s',(id,))
        result : list = cursor.fetchall()
        cursor.close()
        connection.close()
        return result
    
    def delete_device_inforamtions_by_device_id(self, id : str) -> None:
        connection = Connection("monitoring").connection
        cursor = connection.cursor()
        cursor.execute("DELETE FROM iot_information WHERE iot_id LIKE %s",(id))
        connection.commit()
        cursor.close()
    