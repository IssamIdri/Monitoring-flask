from flask import request, render_template, redirect, url_for, session


from app import app
from app.data.models.iot_device_informations import *
from app.data.models.iot_device import *
from geopy.geocoders import Nominatim
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

from datetime import datetime
import paho.mqtt.client as mqtt

import json
from flask_mqtt import Mqtt


app.config['MQTT_BROKER_URL'] = 'test.mosquitto.org'
app.config['MQTT_BROKER_PORT'] =1883
MQTT_TOPIC = 'iot/esisa'

mqtt = Mqtt(app)

@mqtt.on_connect()
def hand_connect(client, userData, flags, rc):
        #je suis connecte
        global connected
        connected = False
        if connected:
            return
        if rc==0:
            print('Connection ')
            mqtt.subscribe(MQTT_TOPIC)
            print(f"Subscribing to topic: {MQTT_TOPIC}")
            connected = True
        else:
            print('Connection refused')
        
         
@mqtt.on_message()
def handle_message(client, userdata, message):
        
        if message.topic == MQTT_TOPIC:
            try:
                payload = json.loads(message.payload.decode())
                temperature = float(payload.get('temperature'))
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                #print(f'Temperature: {temperature}, Timestamp: {timestamp}')
                # Uncomment the following lines when you're ready to test the database insertion
                try :

                   
                        iot_devi_info_service: iot_DeviceInformationsService = iot_DeviceInformationsService()
                        iot_devi_info_service.add_iot_device_inforamtion(temperature,1,timestamp)
                    
                        mqtt._disconnect()
                        #mqtt_data = MQTTData(id=None,client_id=iotdevice_id, temperature=temperature, timestamp=timestamp)
                #MQTTDataDao.insertMQTTData(mqtt_data)
                except Exception as e :
                    print(f"Error processing message: {e}")
                


                print(f'Temperature: {temperature}, Timestamp: {timestamp}')
            
            except Exception as e:
                print(f"Error processing message: {e}")
        else:
            print(f"Received message does not match expected topic: {MQTT_TOPIC}")
            
print("End of script")

@app.route("/show_graphe_iot_device/<id>")
def show_iot_device_info(id: str):
    devi_info_service: iot_DeviceInformationsService = iot_DeviceInformationsService()
    
    # Assuming select_device_info_by_device_id is a method in your service
    device_info: list = devi_info_service.select_iot_device_by_id_device(id)
    
    temperature = [item[1] for item in device_info]
    time = [item[3] for item in device_info]

    return render_template('iot_graph.html', temperature=temperature, time_data=time)





