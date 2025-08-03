import requests
import json
import os
from datetime import datetime

API_KEY = "8c630741ff0563b7632f0e593f87e654" 
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

def get_weather(city, unit='metric'):
    url = f"{BASE_URL}q={city}&appid={API_KEY}&units={unit}"
    try:
        response = requests.get(url)
        response.raise_for_status() 
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except requests.exceptions.ConnectionError:
        print("Network error: Please check your internet connection.")
        return None
    except requests.exceptions.Timeout:
        print("Request timed out. Please try again later.")
        return None
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        return None

    data = response.json()
    if data.get("cod") != 200:
        print(f"Error: {data.get('message')}")
        return None

    local_time = datetime.utcfromtimestamp(data["dt"]).strftime('%Y-%m-%d %H:%M:%S')

    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "description": data["weather"][0]["description"],
        "local_time": local_time 
    }

def save_search_history(city):
    if os.path.exists('search_history.json'):
        with open('search_history.json', 'r') as file:
            history = json.load(file)
    else:
        history = []

    history.append(city)
    
    with open('search_history.json', 'w') as file:
        json.dump(history, file)

def convert_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def display_weather(weather, unit):
    temperature = weather['temperature']
    if unit == 'imperial':
        temperature = convert_to_fahrenheit(temperature)

    temp_unit = "°F" if unit == 'imperial' else "°C"
    
    print(f"City: {weather['city']}")
    print(f"Temperature: {temperature:.2f}{temp_unit}")
    print(f"Humidity: {weather['humidity']}%")
    print(f"Wind Speed: {weather['wind_speed']} m/s")
    print(f"Condition: {weather['description']}")
    print(f"Local Time (UTC): {weather['local_time']}")  