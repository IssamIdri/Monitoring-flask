from app.data.repository.iot_device_informations_repository import iot_DeviceInforamtionsRepository
from datetime import datetime

class iot_DeviceInformationsService :
    def __init__(self) -> None:
        self.iot_dev_info_repo : iot_DeviceInforamtionsRepository = iot_DeviceInforamtionsRepository()

    def add_iot_device_inforamtion(self, temperature:float,iot_id:str,time : datetime) ->None:
        self.iot_dev_info_repo.insert_iot_device_info(temperature,iot_id,time)

    def select_iot_device_by_id_device(self, id : str) -> list:
        return self.iot_dev_info_repo.get_iot_device_inforamtions_by_device_id(id)
    
    def remove_iot_device_by_id_device(self, id : str) -> None:
        self.iot_dev_info_repo.delete_device_inforamtions_by_device_id(id) 

if __name__ == "__main__" :
    pass
