from wiper import set_wiper_value
from mqtt_handle import data_to_json, connect_to_mqtt
from serial_reader import get_data
from sensors_units import sensor_config
from dotenv import load_dotenv

import serial
import os
import json
import threading

# Ladda in miljövariabler
load_dotenv()

broker = os.getenv("MQTT_BROKER")
port = int(os.getenv("MQTT_PORT"))
user = os.getenv("MQTT_USER")
password = os.getenv("MQTT_PASSWORD")

# Anslut till mqtt-broker
mqtt_client = connect_to_mqtt(broker, port, user, password)

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

                print("Data skickad till MQTT:", data)

    except KeyboardInterrupt:
        print("Avslutar serial_to_mqtt...")
    finally:
        ser.close()
        print("Seriell anslutning stängd.")

# Funktion för att hantera wiper-värden
def handle_wiper():
    # 39 := 20.6
    # 40 := 21.1
    # 41 := 21.9
    # 42 := 21.9
    # 43 := 22.0??


    while True:
        try:
            value = int(input("Enter a value between 0 and 127: "))
            set_wiper_value(value)
            print("Wiper value set to", value)
        except ValueError:
            print("Ogiltigt värde! Ange ett tal mellan 0 och 127.")

# Skapa och starta trådar
serial_thread = threading.Thread(target=serial_to_mqtt, daemon=True)
#wiper_thread = threading.Thread(target=handle_wiper, daemon=True)

serial_thread.start()
#wiper_thread.start()

# Håll huvudtråden aktiv
serial_thread.join()
#wiper_thread.join()
