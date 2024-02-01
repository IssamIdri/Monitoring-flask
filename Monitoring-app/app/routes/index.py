from flask import request, render_template
from app import app
from flask import request, render_template
from app.data.models.iot_device import iot_device
from app import app


@app.route('/index', methods=["GET"])
def index():
    if request.method == "GET":
        device_ser : iot_device= iot_device()
        result_iotdata = device_ser.select_all_iot_device()
        print(result_iotdata)
        return render_template("index.html", devices_data=result_iotdata)


    
