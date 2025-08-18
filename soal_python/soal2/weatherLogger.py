from ..function import time_utils

import requests
import json


BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = "79eded02a47bc1a1349983762a977a3f"
CITY_NAME = "Palu"
LOG_FILE = "soal_python/log/weather_data.json"


def fetch(city, api_key):
    params = { "q": city, "appid": api_key, "units": "metric"}
    response = requests.get(BASE_URL, params=params, timeout=10)
    return response.json()
    


def writeJsonFile(weather_data):
    #append new json data to json file
    try:
        with open("soal_python/log/weather_data.json", "r+") as f:
            file_data = json.load(f)
            file_data["weather_data"].append(weather_data)
            f.seek(0)
            json.dump(file_data, f, indent=4)
            f.truncate()
            print("[INFO] Append new JSON data")
    
    #create new json file if it does not exist
    except Exception as e: 
        with open("soal_python/log/weather_data.json", "w+") as f:
            data = {"weather_data":[weather_data]}
            json.dump(data, f, indent=4)
            print("[INFO] New JSON file generated", e)
            
def samplingWeatherData():
    try:
        response = fetch(CITY_NAME, API_KEY)
    except:
        print("[ERROR] Failed to request data from API, check your internet connection")
    else:    
        if (response["cod"] == 200):
            current_temp = response["main"]["temp"]
            current_humidity = response["main"]["humidity"]
            data = {"temp": current_temp, "humidity": current_humidity,
                    "time": time_utils.getTimeinTimezone(7)}
            writeJsonFile(data)
            print(f"{time_utils.getTimeinTimezone(7)} - Success Running Sampling Data Weather with Result Temperature {current_temp} Celsius & Humidity {current_humidity}%")
        else:
            status_code = response["cod"]
            error_message = response["message"]
            print(f"{time_utils.getTimeinTimezone(7)} - Failed Running Sampling Data Weather with Status Code {status_code} - {error_message}")
