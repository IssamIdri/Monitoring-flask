from app.data.mysql.connection import Connection

class DeviceRepository :
    def create_device(self, device_name: str, device_ip: str, device_mac_address: str, type: str) -> None:
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
        cursor.execute('SELECT * FROM iotdevices')
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
        
        '''IOTDEVICES'''
        
    def create_iotdevice(self,name :str, adresse_ip: str, adresse_mac: str, longitude: float, latitude: float) -> None:
            try:
                connection=Connection("monitoring").connection
                cursor =connection.cursor()
                cursor.execute('INSERT INTO iotdevices (name,adresse_ip,adresse_mac,longitude,latitude) VALUES (%s,%s,%s,%f,%f)', (name,adresse_ip,adresse_mac,longitude,latitude))
                connection.commit()
                cursor.close()
                connection.close()
            except Exception as err:
                print(err)
                
    def getiotdevicebyname(self,name : str) -> any:
        connection = Connection("monitoring").connection
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM devices WHERE id = %s', (name,))
        result : any = cursor.fetchone()
        cursor.close()
        connection.close()
        return result
    
    def getalliotdevices(self) -> list:
        connection = Connection("monitoring").connection
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM iotdevices')
        result : list = cursor.fetchall()
        cursor.close()
        connection.close()
        return result
    

if __name__ == "__main__" :
    pass