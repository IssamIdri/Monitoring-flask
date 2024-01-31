from flask import request, render_template, redirect, url_for, session
from app.data.models.iot_device import iot_device
from app.data.models.deviceservices import DeviceService

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


def train_random_forest_model(data):
    data['timestamp'] = data['date'].astype(np.int64) // 10**9  # Extract timestamp in seconds
    data['hour'] = pd.to_datetime(data['date']).dt.hour
    data['day_of_week'] = pd.to_datetime(data['date']).dt.dayofweek
    data['month'] = pd.to_datetime(data['date']).dt.month

    X = data[['timestamp', 'hour', 'day_of_week', 'month']]
    y = data['precipitation']

    # Split the data into training, validation, and test sets
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate on the validation set
    val_predictions = model.predict(X_val)
    val_mse = mean_squared_error(y_val, val_predictions)
    
    # Example of predicting precipitation for the next 7 days
    future_timestamps = pd.date_range(start=pd.Timestamp.now(), periods=7, freq='D')
    future_data = {
        'timestamp': future_timestamps.astype(np.int64) // 10**9,
        'hour': future_timestamps.hour,
        'day_of_week': future_timestamps.dayofweek,
        'month': future_timestamps.month
    }
    future_X = pd.DataFrame(data=future_data)
    predictions = model.predict(future_X)

    # Evaluate on the test set
    test_predictions = model.predict(X_test)
    test_mse = mean_squared_error(y_test, test_predictions)
  

    return model, future_timestamps, predictions

def generate_prediction_graph(dates, predictions):
    plt.figure(figsize=(10, 5))
    plt.plot(dates, predictions, marker='o', linestyle='-', color='b')
    plt.title('7-Day Precipitation Predictions')
    plt.xlabel('Date')
    plt.ylabel('Predicted Probability')
    plt.grid(True)

    # Specify the path where you want to save the graph
    graph_path = "C:/Users/msià/Desktop/python/Monitoring_app/app/static/imgs/prediction_graph.png"  # Change this to your desired path

    plt.savefig(graph_path)
    plt.close()

    return graph_path

def get_lat_long(city):
    geolocator = Nominatim(user_agent="geo_locator")
    location = geolocator.geocode(city)

    if location:
        return location.latitude, location.longitude
    else:
        return None
