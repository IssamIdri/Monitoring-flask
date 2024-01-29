
from flask import request, render_template, redirect

from app.data.services.deviceservices import DeviceService
from app import app
from app.data.snmp_data.testsnmp import snmp_get


'''
@app.route('/snmp', methods=['GET', 'POST'])
def snmp_page():
    if request.method == 'POST':
        # Extract form data
        target = request.form.get('target')
        oid = request.form.get('oid')
        community = request.form.get('community', 'public')
        port = int(request.form.get('port', 161))

        # Perform SNMP GET request
        snmp_data = snmp_get(oid, target, community, port)

        # Extract numerical values using regular expression
        numeric_values = [float(match.group(1)) for match in re.finditer(r'INTEGER: (\d+)', str(snmp_data))]
        print(snmp_data)
        print(numeric_values)  # This will print a list of float values
        return render_template('snmp.html', snmp_data=snmp_data, numeric_values=numeric_values)
    else:
        # Render the SNMP form page
        return render_template('snmp.html', snmp_data=None)
'''



from pysnmp.hlapi import *
import random
from flask import render_template, redirect
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from app import app
import base64
import io
import random
from app.data.services.device_information_sevice import DeviceInformationsService
from app.data.services.deviceservices import DeviceService



# SNMP GET function
def snmp_get(oid, target, community='public', port=161):
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
        return [x[1].prettyPrint() for x in varBinds]

# Route for adding data
@app.route("/add_data", methods=["GET", "POST"])
def add_data():
    if request.method == 'POST':
        device_id = request.form.get('device_id')
        target = request.form.get('target')  # Get the SNMP target from the form

        # Perform SNMP GET for required OIDs using the provided target
        ram_data = snmp_get('.1.3.6.1.2.1.25.2.3.1.6.1', target, community='public')
        cpu_data = snmp_get('.1.3.6.1.2.1.25.3.3.1.2', target, community='public')
        disk_space_used = snmp_get('.1.3.6.1.2.1.25.2.3.1.6.1', target, community='public')
        disk_size = snmp_get('.1.3.6.1.2.1.25.2.3.1.5.1', target, community='public')

        device_ser : DeviceService = DeviceService()
        device_name : str = request.form.get("device_name")
        device_ip : str = request.form.get("target")
        device_mac_address : str = request.form.get("device_mac_address")
        type : str = request.form.get("type")

        device_ser.add_device(device_name, device_ip, device_mac_address, type)

        # In a real-world scenario, you would store this data in your database
        print(f"Device ID: {device_id}, Target: {target}, RAM: {ram_data}, CPU: {cpu_data}, Disk Space Used: {disk_space_used}, Disk Size: {disk_size}")

        return redirect('/show_graph/' + device_id)

    return render_template('add_data.html')  # You need to create an HTML file for this route

# Route for viewing data with a graph
@app.route("/show_graph/<device_id>")
def show_graph(device_id):
    target_ip = request.form.get('target')
    print(target_ip)
    data = mapping_device_info(device_id,target_ip)
    if not data:
        return redirect('/showdevices')

    ram_data, cpu_data, disk_space_used, disk_size = zip(*data)

    fig, ax = plt.subplots()
    ax.plot(ram_data, label='RAM', marker='.')
    ax.plot(cpu_data, label='CPU', marker='.')
    ax.plot(disk_space_used, label='DISK', marker='.')
    ax.plot(disk_size, label='DISK SIZE', marker='.')
    ax.set_xlabel('Time')
    ax.set_ylabel('Utilization (%)')
    ax.set_title('RAM, CPU, and Disk Utilization Over Time')
    ax.legend(loc='center right')

    canvas = FigureCanvas(fig)
    img = io.BytesIO()
    canvas.print_png(img)

    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    device_ser = DeviceService()
    device_info = device_ser.select_device_by_id(device_id)

    return render_template('graphedevices.html', img_base64=img_base64, device_info=device_info)

def bytes_to_gb(bytes_value):
    gb_value = bytes_value / (1024 ** 3)
    return gb_value

# Your existing function for mapping device info
def mapping_device_info(id,target_ip):
    devi_info_service = DeviceInformationsService()
    device_info = devi_info_service.select_device_by_id_device(id)
    device_info = device_info[-30:]

    # Fetch actual data from the target IP using SNMP
    ram_oid = '.1.3.6.1.2.1.25.2.3.1.6.1'  # Adjust the RAM OID as needed
    cpu_oid = '.1.3.6.1.4.1.2021.11.11.0'  # Adjust the CPU OID as needed
    disk_space_used_oid = '.1.3.6.1.2.1.25.2.3.1.6.1'  # Adjust the Disk Space Used OID as needed
    disk_size_oid = '.1.3.6.1.2.1.25.2.3.1.5.1'  # Adjust the Disk Size OID as needed

    ram_data = [snmp_get(ram_oid, target_ip)]  # Adjust snmp_get function accordingly
    cpu_data = [snmp_get(cpu_oid, target_ip)]  # Adjust snmp_get function accordingly
    disk_space_used = [snmp_get(disk_space_used_oid, target_ip)]  # Adjust snmp_get function accordingly
    disk_size = [snmp_get(disk_size_oid, target_ip)]  # Adjust snmp_get function accordingly

    return list(zip(ram_data, cpu_data, disk_space_used, disk_size))


