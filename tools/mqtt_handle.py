from tools.API_tools import average_temperature, average_temperature_weight
from tools.serial_reader import get_data

import serial
import json 
import paho.mqtt.client as mqtt
import os
import time


# Mappings för att mappa index i datan till namn och skala
def data_to_json(data):
    data_dict = {}
    for name, value in data:
        data_dict[name] = value
    return json.dumps(data_dict)

# Anslut till mqtt-broker
def connect_to_mqtt(broker, port, user, password):
    client = mqtt.Client()
    client.username_pw_set(user, password)
    client.connect(broker, port)
    return client

def average_mqtt(mqtt_client):
    while True: 
        state_topic = f"heatpump/sensor/average_temp"
        mqtt_client.publish(state_topic, average_temperature())
        time.sleep(60)

def average_weight_mqtt(mqtt_client):
    global latest_weight
    try: 
        while True: 
            state_topic = f"heatpump/sensor/average_temp"
            mqtt_client.publish(state_topic, round(average_temperature_weight(latest_weight),1))
            time.sleep(60)
    except Exception as e:
        print(f'Something went wrong: {e}')
        time.sleep(300)  # Vänta lite innan nästa försök


# Funktion för att läsa data från serieporten och publicera till MQTT
def serial_to_mqtt(ser,mqtt_client):

    try:
        while True:
            raw_data = ser.readline().decode('utf-8').strip()
            if raw_data:
                data = get_data(raw_data)

                # Skicka varje värde till respektive topic
                for sensor, value in data.items():
                    state_topic = f"heatpump/sensor/{sensor}"
                    mqtt_client.publish(state_topic, value)

                #debug >>print("Data skickad till MQTT:", data)

    except KeyboardInterrupt:
        print("Avslutar serial_to_mqtt...")
    finally:
        ser.close()
        print("Seriell anslutning stängd.")        