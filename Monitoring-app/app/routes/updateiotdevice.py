from flask import render_template, request, redirect

from app.data.IOTservice.iotservice import iotdevice
from app import app


@app.route("/showupdateiotdevice/<id>")
def show_update_iot_device(id : str) :
    device_ser : iotdevice = iotdevice()
    device_info = device_ser.getiotdevicebyid(id)
    return render_template("updateiotdevice.html", device_info = device_info)



@app.route("/updateiotdevice", methods=["POST"])
def update_iot_device() :
    device_ser : iotdevice = iotdevice()
    device_id:str = request.form.get("id")
    device_name:str= request.form.get("name")
    device_ip:str = request.form.get("adresse_ip")
    device_mac_address:str = request.form.get("adresse_mac")
    longitude  = float(request.form.get("longitude"))
    latitude  = float(request.form.get("latitude"))
    device_ser.update_iotdevice(device_id,device_name,device_ip,device_mac_address, longitude,latitude)
    return redirect('/showiotdevices')