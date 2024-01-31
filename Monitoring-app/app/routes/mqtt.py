import requests
from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_mqtt import Mqtt
from flask_migrate import Migrate
import mpld3
import matplotlib.pyplot as plt
from app.data.MQTT.MQTTdb import IOTDevice
from app.data.MQTT.MQTTdb import db
import json
from datetime import datetime
from app import app


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['MQTT_BROKER_URL'] = 'test.mosquitto.org'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 2  
app.config['MQTT_TLS_ENABLED'] = False
app.config['OPENWEATHERMAP_API_KEY'] = 'df4106b5a58e3b3d39785b5b1752bb9d'

db.init_app(app)
mqtt = Mqtt(app)
migrate = Migrate(app, db)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc) :
    mqtt.subscribe('iot/projetesisa')

@mqtt.on_message()
def handle_message(client, userdata, message) :
    topic = message.topic
    payload = message.payload.decode()

    # Analyser le message et extraire les données
    data = json.loads(payload)
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    luminosity = data.get('luminosity')

    # Mettre à jour la base de données
    device = IOTDevice(ip_address=topic, temperature=temperature, humidity=humidity, luminosity=luminosity)
    db.session.add(device)
    db.session.commit()

@app.route('/homemqtt', methods=['GET', 'POST'])
def homemqtt() :
    if request.method == 'POST' :
        ip_address = request.form['ip_address']
        mac_address = request.form['mac_address']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        
        # Convertir la chaîne de date en objet datetime
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()

        # Récupérer les données météorologiques de l'API OpenWeatherMap
        weather_data = get_weather_data(latitude, longitude, date)

        # Enregistrer les données dans la base de données
        new_device = IOTDevice(
            ip_address=ip_address,
            mac_address=mac_address,
            latitude=latitude,
            longitude=longitude,
            temperature=weather_data['temperature'],
            humidity=weather_data['humidity'],
            luminosity=weather_data['luminosity'],
            date=date
        )
        db.session.add(new_device)
        db.session.commit()

    devices = IOTDevice.query.all()
    return render_template('homemqtt.html', devices=devices)

@app.route('/listiotdevices')
def devices() :
    devices = IOTDevice.query.all()
    return render_template('listiotdevices.html', devices=devices)

@app.route('/grapheiotdevice', methods=['POST'])
def plot():
    mac_address = request.form['mac_address']

    # Récupérer les données de la base de données en fonction de l'adresse MAC
    data = IOTDevice.query.filter_by(mac_address=mac_address).all()

    # Créer les listes pour les données
    temperatures = []
    humidity = []
    luminosity = []
    days = []

    # Collecter les données par jour
    for entry in data:
        temperatures.append(entry.temperature)
        humidity.append(entry.humidity)
        luminosity.append(entry.luminosity)
        days.append(entry.date.strftime('%d-%m-%Y'))  # Formatage de la date

    # Créer le graphique avec Matplotlib
    plt.figure(figsize=(12, 8))  # Taille du graphique
    plt.xlabel('Jours')
    plt.ylabel('Données')
    plt.title('Données météorologiques par jour')

    # Affichage de la température
    plt.plot(days, temperatures, color='tab:red', label='Temperature')

    # Affichage de l'humidité
    plt.plot(days, humidity, color='tab:blue', label='Humidité')

    # Affichage de la luminosité
    plt.plot(days, luminosity, color='tab:green', label='Luminosité')

    plt.legend(loc='best')
    plt.xticks(rotation=45, ha='right')  # Rotation des étiquettes des jours
    plt.tight_layout()

    # Convertir le graphique en HTML
    html_graph = mpld3.fig_to_html(plt.gcf())

    return render_template('grapheiotdevice.html', graph=html_graph)

def get_weather_data(latitude, longitude, date):
    api_key = app.config['OPENWEATHERMAP_API_KEY']
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()

    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    luminosity = data['clouds']['all']  # Using cloudiness as an example for luminosity

    return {'temperature': temperature, 'humidity': humidity, 'luminosity': luminosity}

