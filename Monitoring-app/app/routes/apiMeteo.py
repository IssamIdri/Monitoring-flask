import requests
from flask import Flask, render_template, request
from app import app
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime, timedelta
from app import app
import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg'


@app.route('/meteo', methods=['GET', 'POST'])
def meteo():
    if request.method == 'POST':
        city = request.form['city']
        latitude, longitude = get_lat_lon(city)
        temperature = get_temperature(city)
        img_data = getImageData(latitude, longitude)
        return render_template('meteo.html', city=city, img_data=img_data,temperature=temperature)
    return render_template('meteo.html')

def get_temperature(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    api_key = "a783b884be7400e47e8fa2c6c611b734"
    params = {'q': city, 'appid': api_key, 'units': 'metric'}  # Use metric units for Celsius
    response = requests.get(base_url, params=params).json()

    if response['cod'] == '404':
        return 'City not found'
    else:
        temperature = response['main']['temp']
        return temperature
    
def get_lat_lon(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    api_key = "a783b884be7400e47e8fa2c6c611b734"
    params = {'q': city, 'appid': api_key}
    response = requests.get(base_url, params=params).json()
    
    if response['cod'] == '404':
        return None, None
    else:
        latitude = response['coord']['lat']
        longitude = response['coord']['lon']
        return latitude, longitude

def getImageData(latitude, longitude):
    try :
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&past_days=10&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
        weather_data = get_weather_data(api_url)

        if weather_data:
            df = pd.DataFrame(weather_data['hourly'])

            df.set_index('time', inplace=True)

            df.index = pd.to_datetime(df.index)

            start_date = datetime.now() - timedelta(days=10)
            end_date = datetime.now()

            df_interval = df[(df.index >= start_date) & (df.index <= end_date)]

            X_train, X_test, y_train, y_test = train_test_split(df_interval.index, df_interval['temperature_2m'], test_size=0.2, random_state=42)

            predictions = predict_temperature(X_train, y_train, X_test)
            
            return visualize_data(df_interval.index, y_test, predictions)
    except:
        return None
def get_weather_data(api_url):
    try :
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Erreur {response.status_code}: Impossible de récupérer les données météorologiques.")
            print(response.text)
            return None
    except :
        pass

def predict_temperature(X_train, y_train, X_test):
    try:
        model = LinearRegression()

        X_train_numeric = (X_train - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
        X_train_numeric = X_train_numeric.values.reshape(-1, 1)

        model.fit(X_train_numeric, y_train)

        X_test_numeric = (X_test - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
        X_test_numeric = X_test_numeric.values.reshape(-1, 1)

        predictions = model.predict(X_test_numeric)
        return predictions
    except : 
        pass

def visualize_data(dates, actual_temperature, predicted_temperature):
    try:
        plt.figure(figsize=(10, 6))

        dates = dates[:len(actual_temperature)]

        unique_dates = list(set(dates.date))
        unique_dates.sort()

        indices = [i for i, date in enumerate(dates.date) if date in unique_dates]

        plt.plot(dates[indices], actual_temperature[indices], label="Température réelle", marker='o')
        plt.plot(dates[indices], predicted_temperature[indices], label="Prédiction de température", marker='o')


        plt.title('Prédiction de température')
        plt.xlabel('Date')
        plt.ylabel('Température (°C)')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Convertir le graphique en image base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        img_data = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close()

        return img_data
    except :
        pass