from app.data.repository.iot_device_repository import iotDeviceRepository

class iot_device :
    def __init__(self) -> None:
        self.iot_device_repo = iotDeviceRepository()

    def add_iot_device(self, name : str, ip: str, mac_address: str, type : str,adresse : str) -> None:
        try :
            self.iot_device_repo.create_iot_device(name, ip, mac_address, type,adresse)
        except Exception as err: 
            print(err)
    
    def select_iot_device_by_id(self, id : str) -> tuple:
        try :
            return self.iot_device_repo.get_iot_device_by_id(id)
        except :
            return None

    def select_all_iot_device(self):
        try :
            return self.iot_device_repo.get_all_iot_devices()
        except Exception as err: 
            print(err)
            return None

    def delete_iot_device(self, id : str) :
        try :
            self.iot_device_repo.delete_iot_device(id)
        except Exception as err: 
            print(err)
            
    def update_iot_device(self, id :str, name:str, ip:str, mac_address:str, type : str,addresse : str) -> None :
        try :
            self.iot_device_repo.update_iot_device(id, name, ip, mac_address, type,addresse)
        except Exception as err: 
            print(err)        

if __name__ == "__main__" :
    pass

