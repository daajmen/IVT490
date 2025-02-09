from wiper import set_wiper_value
from mqtt_handle import data_to_json, connect_to_mqtt
from serial_reader import get_data
from sensors_units import sensor_config
from API_tools import average_temperature, average_temperature_weight
from dotenv import load_dotenv

import serial
import os
import json
import threading
import time

# Ladda in miljövariabler
load_dotenv()

# Variabel för att lagra det senaste viktvärdet
latest_weight = 100
latest_wiper = 40

# Mappa värden
broker = os.getenv("MQTT_BROKER")
port = int(os.getenv("MQTT_PORT"))
user = os.getenv("MQTT_USER")
password = os.getenv("MQTT_PASSWORD")

# Anslut till mqtt-broker
mqtt_client = connect_to_mqtt(broker, port, user, password)

# Callback-funktion för att hantera inkommande meddelanden
def on_message(client, userdata, message):
    global latest_weight
    
    try:
        # Hantera olika ämnen
        if message.topic == "heatpump/sensor/weight":
            latest_weight = float(message.payload.decode())
            # Uppdatera average temp
            state_topic = f"heatpump/sensor/average_temp"
            mqtt_client.publish(state_topic, round(average_temperature_weight(latest_weight),1))    
            print(f"Viktvärde uppdaterat från MQTT: {latest_weight}")
        
        elif message.topic == "heatpump/sensor/wiper":
            latest_wiper = int(message.payload.decode())
            handle_wiper(latest_wiper)
            print(f"Meddelande från wiper: {latest_wiper}")
            # Hantera other_topic här
    except: 
        print('failure i on_message')


# Sätt callback-funktionen för inkommande meddelanden
mqtt_client.on_message = on_message

# Prenumerera på önskat topic när du ansluter till brokern
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Ansluten till MQTT-broker")
        # Publicera startvärde för vikt
        state_topic = f"heatpump/sensor/weight"
        wiper_topic = f"heatpump/sensor/wiper"
        mqtt_client.publish(state_topic, 100)
        mqtt_client.publish(wiper_topic, 41)
        
        # Prenumerera på alla önskade ämnen
        client.subscribe("heatpump/sensor/weight", qos=1)
        client.subscribe("heatpump/sensor/wiper", qos=1)
        # Lägg till fler prenumerationer här
    else:
        print(f"Misslyckades att ansluta till MQTT-broker. Felkod: {rc}")
# Sätt callback-funktionen för anslutning
mqtt_client.on_connect = on_connect

# Starta MQTT-loopen för att lyssna efter meddelanden
mqtt_client.loop_start()






# Initiera seriell kommunikation
ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)

# Funktion för att publicera Home Assistant Discovery-konfiguration
def publish_discovery_config():
    for sensor, unit in sensor_config.items():
        config_topic = f"homeassistant/sensor/{sensor}/config"
        state_topic = f"heatpump/sensor/{sensor}"
        payload = {
            "name": sensor.replace("_", " ").capitalize(),
            "state_topic": state_topic,
            "unit_of_measurement": unit,
            "value_template": "{{ value }}" if unit else None,
        }
        mqtt_client.publish(config_topic, json.dumps(payload), retain=True)

# Publicera konfiguration vid start
publish_discovery_config()

# Funktion för att läsa data från serieporten och publicera till MQTT
def serial_to_mqtt():
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

# Funktion för att hantera wiper-värden
def handle_wiper(input_value):
    # 39 := 20.6    # 40 := 21.1    # 41 := 21.9    # 42 := 21.9    # 43 := 22.0??
    try:
        set_wiper_value(input_value)
        print("Wiper value set to", input_value)
    except ValueError:
        print("Ogiltigt värde! Ange ett tal mellan 0 och 127.")

def average_mqtt():
    while True: 
        state_topic = f"heatpump/sensor/average_temp"
        mqtt_client.publish(state_topic, average_temperature())
        time.sleep(60)

def average_weight_mqtt():
    global latest_weight
    try: 
        while True: 
            state_topic = f"heatpump/sensor/average_temp"
            mqtt_client.publish(state_topic, round(average_temperature_weight(latest_weight),1))
            # debugprint(f'debug weight: {latest_weight}')
            # debugprint(f'debug average: {average_temperature_weight(latest_weight)}')
            time.sleep(60)
    except: 
        print('Something went wrong') 



# Skapa och starta trådar
serial_thread = threading.Thread(target=serial_to_mqtt, daemon=True)
average = threading.Thread(target=average_weight_mqtt, daemon=True)

#wiper_thread = threading.Thread(target=handle_wiper, daemon=True)

serial_thread.start()
average.start()
#wiper_thread.start()

# Håll huvudtråden aktiv
serial_thread.join()
average.join()
#wiper_thread.join()
