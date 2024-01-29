from flask import request, render_template
from app.data.services.deviceservices import DeviceService
from app import app


@app.route("/showiotdevices", methods=["GET"])
def show_iot_devices() :
    if request.method == "GET" :
        device_ser : DeviceService = DeviceService()
        result_iotdata : list = device_ser.selectinfoiot()
        return render_template("showiotdevices.html", devices_data = result_iotdata)