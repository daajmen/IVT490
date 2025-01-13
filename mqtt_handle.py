import json 
import paho.mqtt.client as mqtt
import os

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

