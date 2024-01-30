from flask import request, render_template, redirect

from app.data.IOTservice.iotservice import iotdevice
from app import app


@app.route("/addiotdevice", methods=["GET", "POST"])
def addiotdevice() :
    if request.method == "GET" :
        return render_template("addiotdevice.html")
    
    else :
        device_ser : iotdevice = iotdevice()
        device_name : str = request.form.get("name")
        device_ip : str = request.form.get("adresse_ip")
        device_mac_address : str = request.form.get("adresse_mac")
        device_longitude= float(request.form.get("longitude"))
        device_latitude= float(request.form.get("latitude"))
        print(device_name,device_ip,device_mac_address,device_longitude,device_latitude)
        device_ser.add_iotdevice(device_name, device_ip, device_mac_address, device_longitude, device_latitude)
        return redirect('/showiotdevices')