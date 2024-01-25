from flask import request, render_template, redirect

from app.data.services.deviceservices import DeviceService
from app import app


@app.route("/adddevice", methods=["GET", "POST"])
def adddevice() :
    if request.method == "GET" :
        return render_template("adddevice.html")
    
    else :
        device_ser : DeviceService = DeviceService()
        device_name : str = request.form.get("device_name")
        device_ip : str = request.form.get("device_ip")
        device_mac_address : str = request.form.get("device_mac_address")
 

        device_ser.add_device(device_name, device_ip, device_mac_address)
        return redirect('/showdevices')