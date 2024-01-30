from flask import request, render_template
from app import app
from flask import request, render_template
from app.data.IOTservice.iotservice import iotdevice
from app import app


@app.route('/index', methods=["GET"])
def index():
    if request.method == "GET":
        device_ser : iotdevice= iotdevice()
        result_iotdata = device_ser.getalliotdevices()
        print(result_iotdata)
        return render_template("index.html", devices_data=result_iotdata)


    
