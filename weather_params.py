import os
from dotenv import load_dotenv
import requests

load_dotenv()
WEATHER_API = os.getenv('WEATHER_API')

def get_weather_params(q):
    URL = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API}&q={q}&aqi=no"
    r = requests.get(url = URL)
    data = r.json()
    location = data['location']['name']
    temp = data['current']['temp_f']
    humidity = data['current']['humidity']
    precipitation = data['current']['precip_in']
    return (location, temp, humidity, precipitation)
