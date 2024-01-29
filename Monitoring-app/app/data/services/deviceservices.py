from app.data.repository.devicerepository import DeviceRepository

class DeviceService :
    def __init__(self) -> None:
        self.device_repo = DeviceRepository()

    def add_device(self, device_name: str, device_ip: str, device_mac_address: str, type: str) -> None:
        try :
            self.device_repo.create_device(device_name, device_ip, device_mac_address, type)
        except Exception as err: 
            print(err)
    
    
    def select_device_by_id(self, device_id : str) -> tuple:
        try :
            return self.device_repo.get_device_by_id(device_id)
        except :
            return None

    def select_all_device(self):
        try :
            return self.device_repo.get_all_devices()
        except Exception as err: 
            print(err)
            return None

    def delete_device(self, device_id : str) :
        try :
            self.device_repo.delete_device(device_id)
        except Exception as err: 
            print(err)
            
    def update_device(self, device_id :str, device_name:str, device_ip:str, device_mac_address:str, type : str) -> None :
        try :
            self.device_repo.update_device(device_id, device_name, device_ip, device_mac_address, type)
        except Exception as err: 
            print(err)    
            
            '''IOTDEVICES'''    

    def add_iotdevice(self, name: str, adresse_ip: str, adresse_mac: str, longitude: float, latitude: float) -> None:
        try :
            self.device_repo.create_iotdevice(name,adresse_ip,adresse_mac,longitude,latitude)
        except Exception as err: 
            print(err)
    
    def selectinfoiot(self):
        try:
            self.device_repo.getalliotdevices()
        except Exception as err:
            print(err)
            
            
if __name__ == "__main__" :
    pass