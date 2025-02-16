from tools.wiper import handle_wiper
from tools.mqtt_handle import connect_to_mqtt, average_weight_mqtt, serial_to_mqtt, average_mqtt
from assets.sensors_units import sensor_config
from tools.API_tools import average_temperature_weight, publish_discovery_config, fetch_value
from tools.optimization import correction_wiper
from dotenv import load_dotenv

import serial
import os
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
            #state_topic = f"heatpump/sensor/average_temp"
            #mqtt_client.publish(state_topic, round(average_temperature_weight(latest_weight),1))    
            print(f"Viktvärde uppdaterat från MQTT: {latest_weight}")
        
        #elif message.topic == "heatpump/sensor/wiper":
        #    latest_wiper = int(message.payload.decode())
        #    handle_wiper(latest_wiper)
        #    print(f"Meddelande från wiper: {latest_wiper}")
        #    # Hantera other_topic här
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
        mqtt_client.publish(state_topic, 50)
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

# Publicera konfiguration vid start
publish_discovery_config(mqtt_client)

# Initiera seriell kommunikation
ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)    


#Hantering optimering
def run_optimization(room, average): 
    global latest_wiper
    try:
        latest_wiper = handle_wiper(correction_wiper(latest_wiper, room, average))
       #print(f'Wiper värde : {latest_wiper}')
       #print(f'Värmepumpsgivare : {room}')
       #print(f'Medelvärde via HA : {average}')
        time.sleep(300)
    except Exception as e:
        print(f'Something went wrong: {e}')

def run_optimization_loop():
    while True:
        try:
            room_temp = float(fetch_value('sensor.roomtemp'))
            avg_temp = float(fetch_value('sensor.average_temp'))
            run_optimization(room_temp, avg_temp)
        except Exception as e:
            print(f"Fel i optimization loop: {e}")
            print("Väntar 60 sekunder innan nästa försök...")
            time.sleep(60)

def average_calculation(mqtt_client): 
    global latest_weight
    while True: 
        try:
            average_mqtt(mqtt_client)
            time.sleep(60)
        except Exception as e:
            print(f"Fel i average calculation: {e}")
            print("Väntar 60 sekunder innan nästa försök...")
            time.sleep(60)

# Skapa och starta trådar
serial_thread = threading.Thread(target=lambda: serial_to_mqtt(ser, mqtt_client), daemon=True)
average = threading.Thread(target=lambda: average_calculation(mqtt_client), daemon=True)
opti = threading.Thread(target=run_optimization_loop, daemon=True)

serial_thread.start()
average.start()
opti.start()

serial_thread.join()
average.join()
opti.join()
