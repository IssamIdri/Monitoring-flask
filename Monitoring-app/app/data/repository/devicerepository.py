from app.data.mysql.connection import Connection

class DeviceRepository :
    def create_device(self, device_name : str, device_ip: str, device_mac_address: str, type : str) -> None:
        try :
            connection = Connection("monitoring").connection
            cursor = connection.cursor()
            cursor.execute('INSERT INTO devices (device_name, device_ip, device_mac_address, type) VALUES (%s, %s, %s, %s)', (device_name, device_ip, device_mac_address, type))
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as err:
            print(err)


    def get_device_by_id(self, device_id : str) -> any:
        connection = Connection("monitoring").connection
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM devices WHERE id = %s', (device_id,))
        result : any = cursor.fetchone()
        cursor.close()
        connection.close()
        return result

    def get_all_devices(self) -> list:
        connection = Connection("monitoring").connection
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM devices')
        result : list = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

    def update_device(self, device_id :str, device_name:str, device_ip:str, device_mac_address:str, type : str) -> None:
        connection = Connection("monitoring").connection
        cursor = connection.cursor()
        cursor.execute('UPDATE devices SET device_name=%s, device_ip=%s, device_mac_address=%s, type=%s WHERE id=%s', (device_name, device_ip, device_mac_address, type, device_id))
        connection.commit()
        cursor.close()
        connection.close()

    def delete_device(self, device_id:str):
        connection = Connection("monitoring").connection
        cursor = connection.cursor()
        query = 'DELETE FROM devices WHERE id = %s'
        cursor.execute(query, (device_id,))
        connection.commit()
        cursor.close()
        connection.close()


if __name__ == "__main__" :
    pass