from pysnmp .hlapi import *

class SnmpData :
    @staticmethod
    def load_information_by_oid(oid : str, host : str, community='public') :
        total: int = 0
        for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(
            SnmpEngine(),
            CommunityData(community, mpModel=0),
            UdpTransportTarget((host, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(oid)),
            lexicographicMode=False
         ):
            if errorIndication:
                print(f"Error: {errorIndication}")
                break
            elif errorStatus:
                print(f"Error: {errorStatus}")
                break
            else:
                for varBind in varBinds:
                    total += int(varBind[1])

        return total


if __name__ == "__main__" :
    print(SnmpData.load_information_bu_oid("","127.0.0.1"))
