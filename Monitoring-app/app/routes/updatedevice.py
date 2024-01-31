from flask import render_template, request, redirect

from app.data.models.deviceservices import DeviceService
from app import app


@app.route("/showupdatedevice/<id>")
def show_update_device(id : str) :
    device_ser : DeviceService = DeviceService()
    device_info = device_ser.select_device_by_id(id)
    return render_template("updatedevice.html", device_info = device_info)



@app.route("/updatedevice", methods=["POST"])
def update_device() :
    device_ser : DeviceService = DeviceService()
    device_id:str = request.form.get("device_id")
    device_name:str= request.form.get("device_name")
    device_ip:str = request.form.get("device_ip")
    device_mac_address:str = request.form.get("device_mac_address")
    type : str = request.form.get("type")
    device_ser.update_device(device_id,device_name,device_ip,device_mac_address, type)
    return redirect('/showdevices')
