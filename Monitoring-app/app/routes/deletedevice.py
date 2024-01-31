from flask import render_template, redirect

from app.data.models.deviceservices import DeviceService
from app.data.models.device_information_sevice import DeviceInformationsService

from app import app



@app.route('/showdeletedevice/<id>')
def show_device_delete(id : str) :
    device_ser : DeviceService = DeviceService()
    device_info = device_ser.select_device_by_id(id)
    return render_template("deletedevice.html", device_info = device_info)


@app.route('/deletedevice/<id>')
def delete_device(id : str) :
    device_ser : DeviceService = DeviceService()
    device_info_ser : DeviceInformationsService = DeviceInformationsService()
    device_info_ser.remove_device_by_id_device(id)
    device_ser.delete_device(id)
    return redirect('/showdevices')

