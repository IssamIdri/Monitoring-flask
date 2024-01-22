from app.data.repository.device_informations_repository import DeviceInforamtionsRepository

class DeviceInformationsService :
    def __init__(self) -> None:
        self.dev_info_repo : DeviceInforamtionsRepository = DeviceInforamtionsRepository()

    def add_device_inforamtion(self, memory_usage : str, cpu_usage : str, disk_space_used : str,disk_size : str, device_id : str) ->None:
        self.dev_info_repo.insert_device_info(memory_usage, cpu_usage, disk_space_used,disk_size, device_id)

    def select_device_by_id_device(self, device_id : str) -> list:
        return self.dev_info_repo.get_device_inforamtions_by_device_id(device_id)

if __name__ == "__main__" :
    pass
