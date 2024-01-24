from flask import request, render_template
from app.data.services.deviceservices import DeviceService
from app import app


@app.route("/show_devices", methods=["GET"])
def show_devices() :
    if request.method == "GET" :
        device_ser : DeviceService = DeviceService()
        result_data : list = device_ser.select_all_device()
        return render_template("show_devices.html", devices_data = result_data)