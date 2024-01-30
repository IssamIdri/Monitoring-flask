import requests

base_url ="http://api.openweathermap.org/data/2.5/weather?"
api_key="a783b884be7400e47e8fa2c6c611b734"
city="New York"

url = base_url +"appid=" + api_key +"&q=" + city
response = requests.get(url).json()
print(response)

