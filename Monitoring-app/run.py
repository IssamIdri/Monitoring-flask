from app.data.snmp_data.regitredatasnmp import LoadDataBySnmpInfo
from app.data.MQTT.brokermqtt import TemperatureReceiver
from app.data.MQTT.publishermqtt import message
from config import DEBUG, HOST
from app import app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.data.MQTT.MQTTdb import IOTDevice  # Import your model



if __name__ == '__main__':
    LoadDataBySnmpInfo().start()
    #TemperatureReceiver("iot/esisa/test").connect()
    app.run(debug=DEBUG, host=HOST)
