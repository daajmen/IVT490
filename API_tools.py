import datetime
import requests 
from secret import API_KEY

def fetch_value(entity):

    url = f"http://192.168.50.11:8123/api/states/{entity}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "content-type": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['state']
    else: 
        print('failed.')

def average_temperature():
    temp_lower_floor = float(fetch_value('sensor.nedre_vaning_temperatur')) 
    temp_upper_floor = float(fetch_value('sensor.ovre_vaning_temperatur'))
    return (temp_lower_floor + temp_upper_floor) / 2

def average_temperature_weight(input_weight):
    temp_lower_floor = float(fetch_value('sensor.nedre_vaning_temperatur')) 
    temp_upper_floor = float(fetch_value('sensor.ovre_vaning_temperatur'))

    weight = ((100 - input_weight) * 0.01)

    return (weight * temp_upper_floor) + ((1 - weight) * temp_lower_floor)


