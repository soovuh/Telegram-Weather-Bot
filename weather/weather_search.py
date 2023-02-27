import requests
import time
from mtranslate import translate
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
        return None, None

async def get_city(lat, lon):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key_weather}'

    response = requests.get(url)
    response.raise_for_status()
    if response.status_code == 200:
        # Extract relevant data from API response
        data = response.json()
        city = data['name']
        return city
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
        
        print(description)
        translate_description = await translate_to_ua(description)
        time.sleep(0.2)
        weather_str = f'{city.capitalize()}.\n{translate_description.capitalize()},  {(temperature - 273.15):.1f}°C.'
        weather_str.replace('weather condition', '')
        return weather_str, url_icon
    else:
        # Handle API error
        error_str = f'Упс, щось пішло не так... Перевірте, чи корректно ви зареєстрували місце для отримання погоди або спробуйте трохи пізніше'
        return error_str, 'https://cdn0.iconfinder.com/data/icons/shift-interfaces/32/Error-512.png'


# function to translate english string to ukrainian
async def translate_to_ua(text):
    time.sleep(0.3)
    translation = translate(text, 'uk')
    time.sleep(0.3)
    if translation:
        return translation
    else:
        return 'Сталася помилка, спробуйте переєструвати місце, чи повотріть спробу трохи пізніше'


