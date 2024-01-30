from flask import request, render_template
from app.data.IOTservice.iotservice import iotdevice
from app import app


@app.route("/showiotdevices", methods=["GET"])
def show_iot_devices() :
    if request.method == "GET" :
        device_ser : iotdevice = iotdevice()
        result_iotdata : list = device_ser.getalliotdevices()
        
        return render_template("showiotdevices.html", devices_data = result_iotdata)