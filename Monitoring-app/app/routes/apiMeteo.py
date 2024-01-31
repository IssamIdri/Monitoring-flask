import requests

base_url ="http://api.openweathermap.org/data/2.5/weather?"
api_key="df4106b5a58e3b3d39785b5b1752bb9d"
city="New York"

url = base_url +"appid=" + api_key +"&q=" + city
response = requests.get(url).json()
print(response)

