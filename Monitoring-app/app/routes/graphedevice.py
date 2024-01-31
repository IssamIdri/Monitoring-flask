from app.data.models.device_information_sevice import DeviceInformationsService
from app.data.models.deviceservices import DeviceService


from flask import render_template, redirect
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from app import app
import base64
import io
import random

def bytes_to_gb(bytes_value):
    gb_value = bytes_value / (1024 ** 3)
    return gb_value

def mapping_device_info(id : str) -> list:
    devi_info_service : DeviceInformationsService = DeviceInformationsService()
    device_info : list = devi_info_service.select_device_by_id_device(id)
    device_info = device_info[-30:]

    ram_data = [(bytes_to_gb(item[1]) + random.uniform(1, 10)) for item in device_info]
    cpu_data = [item[2] for item in device_info]
    disk_space_used = [bytes_to_gb(item[3]) + random.uniform(1, 50) for item in device_info]
    disk_size = [bytes_to_gb(item[5]) + random.uniform(1, 100) for item in device_info]


    return list(zip( ram_data, cpu_data, disk_space_used,disk_size))


@app.route("/graphedevice/<id>")
def showgraphedevice(id: str):
    data = mapping_device_info(id)
    if(len(data) == 0) :
        return redirect('/showdevices')
    ram_data, cpu_data, disk_space_used, disk_size = zip(*data)
    fig, ax = plt.subplots()

    ax.plot(ram_data, label='RAM', marker='.')
    ax.plot(cpu_data, label='CPU', marker='.')
    ax.plot(disk_space_used, label='DISK', marker='.')
    ax.plot(disk_size, label='CAPACITY', marker='.')
    ax.set_xlabel('Temps')
    ax.set_ylabel('Utilisation (%)')
    ax.set_title('Utilisation de la RAM, du CPU et de l\'espace disque au fil du temps')
    ax.legend(loc='center right')

    canvas = FigureCanvas(fig)
    img = io.BytesIO()
    canvas.print_png(img)

    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    device_ser : DeviceService = DeviceService()
    device_info = device_ser.select_device_by_id(id)

    return render_template('graphedevice.html', img_base64=img_base64, device_info= device_info)

