from app.data.snmp_data.getinformationsnmp import SnmpData

class SnmpService :
    @staticmethod
    def get_total_cpu(ip_adresse : str) -> None:
        return SnmpData.load_information_by_oid("1.3.6.1.2.1.25.3.3.1.2", ip_adresse)
    
    @staticmethod
    def get_total_disk(ip_adresse : str) -> None:
        return SnmpData.load_information_by_oid("1.3.6.1.2.1.25.2.3.1.5", ip_adresse)
    
    @staticmethod 
    def get_totale_size_used_on_disk(ip_adresse : str) -> None:
        return SnmpData.load_information_by_oid("1.3.6.1.2.1.25.2.3.1.6", ip_adresse)
    
    @staticmethod
    def get_totale_ram(ip_adresse : str) -> None:
        return SnmpData.load_information_by_oid("1.3.6.1.2.1.25.2.3.1.5", ip_adresse)
    
    @staticmethod 
    def construction_snmp_object(ip_adresse : str):
        return {
            "cpu" : str(SnmpService.get_total_cpu(ip_adresse)),
            "disk" : str(SnmpService.get_total_disk(ip_adresse)),
            "used_disk" : str(SnmpService.get_totale_size_used_on_disk(ip_adresse)),
            "ram" : str(SnmpService.get_totale_ram(ip_adresse))
        }
    

if __name__ == "__main__" :
    print(SnmpService.construction_snmp_object("127.0.0.1"))