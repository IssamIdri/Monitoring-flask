import threading
import time
from app.data.services.deviceservices import DeviceService
from app.data.services.device_information_sevice import DeviceInformationsService
from app.data.snmp_data.snmpservice import SnmpService

class LoadDataBySnmpInfo(threading.Thread) :
    def __init__(self) -> None:
        super().__init__()
        self.dev_info_service : DeviceInformationsService = DeviceInformationsService()
        

    def run(self):
        while(True) :
            self.dev_service : DeviceService = DeviceService()
            devices_listes : list = self.dev_service.select_all_device()
            for device in devices_listes :
                data_snmp : dict = SnmpService.construction_snmp_object(device[2])
                self.dev_info_service.add_device_inforamtion(
                    data_snmp["ram"], data_snmp["cpu"],data_snmp["used_disk"],data_snmp["disk"],str(device[0])
                )
                time.sleep(60)
            time.sleep(secs=60)


if __name__ == "__main__" :
    pass