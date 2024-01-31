import requests
from flask import Flask, render_template, request
from app import app

@app.route('/meteo', methods=['GET', 'POST'])
def meteo():
    if request.method == 'POST':
        city = request.form['city']
        temperature = get_temperature(city)
        return render_template('meteo.html', city=city, temperature=temperature)
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


