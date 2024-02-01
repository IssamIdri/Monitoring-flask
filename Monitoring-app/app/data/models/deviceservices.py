from app.data.repository.devicerepository import DeviceRepository
import subprocess
import re

class DeviceService :
    def __init__(self) -> None:
        self.device_repo = DeviceRepository()

    
    def snmp_check(self,ip_address:str):
        # Construct the snmpget command for sysDescr
        snmpget_cmd = ['snmpget', '-v2c', '-c', 'public', ip_address, 'sysDescr.0']

        try:
            # Execute the snmpget command and capture the output
            result = subprocess.check_output(snmpget_cmd, universal_newlines=True)

            # Check if the result contains 'No Such Object available on this agent at this OID'
            if 'No Such Object available' in result:
                print(f"SNMP not available on {ip_address}")
                return False

            print(f"SNMP available on {ip_address}")
            return True

        except subprocess.CalledProcessError as e:
            # Handle any errors that may occur during execution
            print(f"Error executing snmpget: {e}")
            return False

        
    def add_device(self, device_name: str, device_ip: str, device_mac_address: str, type: str) -> None:
        try:
            # Check SNMP availability before adding to the database
            if not self.snmp_check(device_ip):
                print(f"SNMP check failed for {device_ip}. Device not added to the database.")
                return

            # SNMP check successful, proceed to add device to the database
            self.device_repo.create_device(device_name, device_ip, device_mac_address, type)
            print(f"Device added successfully: {device_name} - {device_ip}")

        except Exception as err:
            print(f"Error adding device: {err}")
    
    
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
            
           

    
if __name__ == "__main__" :
    pass