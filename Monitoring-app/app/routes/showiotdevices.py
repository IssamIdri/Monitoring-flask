from flask import request, render_template
from app.data.models.iot_device import iot_device
from app import app


@app.route("/showiotdevices", methods=["GET"])
def show_iot_devices() :
    if request.method == "GET" :
        device_ser : iot_device = iot_device()
        result_iotdata : list = device_ser.select_all_iot_device()
        
        return render_template("showiotdevices.html", devices_data = result_iotdata)
    



