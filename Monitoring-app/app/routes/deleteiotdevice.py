from flask import redirect, render_template
from app.data.IOTservice.iotservice import iotdevice
from app import app



@app.route('/showdeleteiotdevice/<id>')
def show_device_iot_delete(id : str) :
    device_ser : iotdevice = iotdevice()
    device_info = device_ser.getiotdevicebyid(id)
    return render_template("deleteiotdevice.html", device_info = device_info)


@app.route('/deleteiotdevice/<id>')
def delete_iot_device(id : str) :
    device_ser : iotdevice = iotdevice()
    device_ser.delete_iotdevice(id)
    return redirect('/showiotdevices')

