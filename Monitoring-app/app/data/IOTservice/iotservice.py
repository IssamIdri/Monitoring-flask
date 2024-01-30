from app.data.mysql.connection import Connection

class iotdevice:
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
                
    def getiotdevicebyname(self,id : int) -> any:
        connection = Connection("monitoring").connection
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM iotdevices WHERE id = %d', (id))
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
    
    def add_iotdevice(self, name: str, adresse_ip: str, adresse_mac: str, longitude: float, latitude: float) -> None:
        try :
            self.create_iotdevice(name,adresse_ip,adresse_mac,longitude,latitude)
        except Exception as err: 
            print(err)
    
    def selectinfoiot(self):
        try:
            self.getalliotdevices()
        except Exception as err:
            print(err)
            
            
    if __name__ == "__main__" :
     pass