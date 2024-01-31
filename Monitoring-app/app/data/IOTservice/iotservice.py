from app.data.mysql.connection import Connection

class iotdevice:
    def create_iotdevice(self,name :str, adresse_ip: str, adresse_mac: str, longitude: float, latitude: float) -> None:
            try:
                connection=Connection("monitoring").connection
                cursor =connection.cursor()
                cursor.execute('INSERT INTO iotdevices (name,adresse_ip,adresse_mac,longitude,latitude) VALUES (%s,%s,%s,%s,%s)', (name,adresse_ip,adresse_mac,longitude,latitude))
                connection.commit()
                cursor.close()
                connection.close()
            except Exception as err:
                print(err)
    
    def update_iotdevice(self, id: int, name: str, adresse_ip: str, adresse_mac: str, longitude: float, latitude: float) -> None:
        connection = Connection("monitoring").connection
        cursor = connection.cursor()
        cursor.execute('UPDATE iotdevices SET name=%s, adresse_ip=%s, adresse_mac=%s, longitude=%s ,latitude=%s WHERE id=%s', (id, name, adresse_ip, adresse_mac, longitude, latitude))
        connection.commit()
        cursor.close()
        connection.close()

    def delete_iotdevice(self, id:str):
        connection = Connection("monitoring").connection
        cursor = connection.cursor()
        query = 'DELETE FROM iotdevices WHERE id = %s'
        cursor.execute(query, (id,))
        connection.commit()
        cursor.close()
        connection.close()
        
              
    def getiotdevicebyid(self,id : int) -> any:
        connection = Connection("monitoring").connection
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM iotdevices WHERE id = %d', (id))
        result : any = cursor.fetchone()
        cursor.close()
        connection.close()
        return result
    
    def getalliotdevices(self) -> list:
        try:
            connection = Connection("monitoring").connection
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM iotdevices')
            result : list = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error fetching data from database: {e}")
        finally:
            cursor.close()
            connection.close()
    
    
    def add_iotdevice(self, name: str, adresse_ip: str, adresse_mac: str, longitude: float, latitude: float) -> None:
        try :
            self.create_iotdevice(name,adresse_ip,adresse_mac,longitude,latitude)
        except Exception as err: 
            print(err)
            
    
    def insert_iotdevice_info(self, temperature : str,id_device: int) -> None:
        connection = Connection("monitoring").connection
        cursor = connection.cursor()
        cursor.execute(
            '''INSERT INTO iot_device_infos (temperature,id_device)
            VALUES (%s, %s)''', (temperature,id_device))
        connection.commit()
        cursor.close()
        connection.close()
        
    def add_iotdevice_inforamtion(self, temperature : str,id_device : int) ->None:
        self.insert_iotdevice_info(temperature,id_device)
    
    
    
    
            
    if __name__ == "__main__" :
     pass