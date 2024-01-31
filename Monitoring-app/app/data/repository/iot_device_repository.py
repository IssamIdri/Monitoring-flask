from app.data.mysql.connection import Connection

class iotDeviceRepository :
    def create_iot_device(self, name : str, adresse_ip: str, adresse_mac: str, longitude : str,latitude : str) -> None:
        try :
            connection = Connection("monitoring").connection
            cursor = connection.cursor()
            cursor.execute('INSERT INTO iotdevices (name, adresse_ip, adresse_mac, longitude,latitude) VALUES (%s, %s, %s, %s, %s)', (name, adresse_ip, adresse_mac, longitude,latitude))
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as err:
            print(err)

    def get_iot_device_by_id(self, id : str) -> any:
        connection = Connection("monitoring").connection
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM iotdevices WHERE id = %s', (id,))
        result : any = cursor.fetchone()
        cursor.close()
        connection.close()
        return result

    def get_all_iot_devices(self) -> list:
        connection = Connection("monitoring").connection
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM iotdevices')
        result : list = cursor.fetchall()
       
        cursor.close()
        connection.close()
        return result

    def update_iot_device(self, id: str, name: str, adresse_ip: str, adresse_mac: str, longitude: str, latitude: str) -> None:
     try:
        connection = Connection("monitoring").connection
        cursor = connection.cursor()
        
        # Using parameterized query
        cursor.execute(
            'UPDATE iot_devices SET name=%s, adresse_ip=%s, adresse_mac=%s, longitude=%s, latitude=%s WHERE id=%s',
            (name, adresse_ip, adresse_mac, longitude, latitude, id)
        )
        
        connection.commit()
     except Exception as e:
        # Handle exceptions (print or log the error, or raise an exception)
        print(f"Error updating device: {e}")
     finally:
        cursor.close()
        connection.close()


    def delete_iot_device(self, id:str):
        connection = Connection("monitoring").connection
        cursor = connection.cursor()
        query = 'DELETE FROM iotdevices WHERE id = %s'
        cursor.execute(query, (id,))
        connection.commit()
        cursor.close()
        connection.close()

if __name__ == "__main__" :
    pass