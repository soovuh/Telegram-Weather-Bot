import requests
import time
from translate import Translator
from config import api_key_cords, api_key_weather

# function for getting cords of city
async def get_cords(city):
    # Replace with your OpenCage Geocoder API key
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city}&key={api_key_cords}"
    response = requests.get(url).json()

    if response["status"]["code"] == 200:
        lat = response["results"][0]["geometry"]["lat"]
        lon = response["results"][0]["geometry"]["lng"]
        return lat, lon
    else:
        return None


# function for getting weather in string format
async def get_weather(lat, lon, city):
    # Replace with your actual API key from OpenWeatherMap
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key_weather}'

    response = requests.get(url)
    response.raise_for_status()
    if response.status_code == 200:
        # Extract relevant data from API response
        data = response.json()
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        weather_icon = data['weather'][0]['icon']
        url_icon = f'http://openweathermap.org/img/w/{weather_icon}.png'
        
        # Format weather information as ordered string
        weather_str = f'Weather for {city}: \n{description.capitalize()}\nTemperature is {(temperature - 273.15):.1f}°C'
        return weather_str, url_icon
    else:
        # Handle API error
        error_str = f'Error retrieving weather information.'
        return error_str


# function to translate english string to ukrainian
async def translate_to_ua(text):
    translator = Translator(to_lang="uk")
    time.sleep(0.3)
    translation = translator.translate(text)
    time.sleep(0.3)
    return translation


