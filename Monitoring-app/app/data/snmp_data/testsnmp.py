from pysnmp.hlapi import *
import os
import subprocess
# Function to perform an SNMP GET request
def snmp_get(oid, target, community='public', port=161):
     # Construct the snmpwalk command
    snmpwalk_command = f"snmpwalk -v2c -c {community} {target} {oid}"

    try:
        # Run the snmpwalk command and capture the output
        result = subprocess.check_output(snmpwalk_command, shell=True, universal_newlines=True)
        print(snmpwalk_command,result)
        return result
    except subprocess.CalledProcessError as e:
        # Handle any errors that occurred during the command execution
        # return f"Error: {e}"
        iterator = getCmd(
            SnmpEngine(),
            CommunityData(community),
            UdpTransportTarget((target, port)),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )

        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
            ))
        else:
            for varBind in varBinds:
                print(' = '.join([x.prettyPrint() for x in varBind]))

    print('SNMP GET function has been created.')