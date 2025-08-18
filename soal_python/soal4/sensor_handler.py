from ..function import time_utils
import json
import random
import csv

def get_sensor_data():
    with open("soal_python/log/weather_data.json", "r") as f:
        file_data = json.load(f)
        
    sensor1 = random.randrange(0, 100)
    sensor2 = round(random.uniform(0, 1000), 2)
    sensor3 = random.choice([True, False])
    sensor4 = file_data["weather_data"][-1]["temp"]
    sensor5 = file_data["weather_data"][-1]["humidity"]
    
    return [sensor1, sensor2, sensor3, sensor4, sensor5]

def log_to_csv(data, status):
    with open("soal_python/log/mqtt_log_180825.csv", "a", newline="") as csvfile:
        fieldnames = ["timestamp", "sensor1", "sensor2",
                      "sensor3", "sensor4", "sensor5", "status"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
        # status = "success" if status == True else "failed"
        row = {
            "timestamp": time_utils.getTimeinTimezone(7), 
            "sensor1": data[0], 
            "sensor2": data[1], 
            "sensor3": data[2], 
            "sensor4": data[3], 
            "sensor5": data[4], 
            "status": status
            }
        writer.writerow(row)