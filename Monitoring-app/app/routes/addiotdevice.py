from flask import request, render_template, redirect

from app.data.models.iot_device import iot_device
from app import app


@app.route("/addiotdevice", methods=["GET", "POST"])
def addiotdevice() :
    if request.method == "GET" :
        return render_template("addiotdevice.html")
    
    else :
        device_ser : iot_device = iot_device()
        device_name : str = request.form.get("name")
        device_ip : str = request.form.get("adresse_ip")
        device_mac_address : str = request.form.get("adresse_mac")
        device_longitude= float(request.form.get("longitude"))
        device_latitude= float(request.form.get("latitude"))
        print(device_name,device_ip,device_mac_address,device_longitude,device_latitude)
        device_ser.add_iot_device(device_name, device_ip, device_mac_address, device_longitude, device_latitude)
        return redirect('/showiotdevices')