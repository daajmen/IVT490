from wiper import set_wiper_value
from mqtt_handle import data_to_json, connect_to_mqtt
from serial_reader import get_data
from dotenv import load_dotenv

import serial

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

# Läs data från serieporten och skriv ut
try:
    while True:
        raw_data = ser.readline().decode('utf-8').strip()
        if raw_data:
            data = get_data(raw_data)
            json_data = data_to_json(data)

            # Skicka data till mqtt-broker
            mqtt_client.publish("heatpump/data", json_data)
            print('Data sent to mqtt:', json_data)

except KeyboardInterrupt:
    print("Avslutar...")
finally:
    ser.close()
    print("Seriell anslutning stängd.")














#while True:
#    value = int(input("Enter a value between 0 and 127: "))
#    set_wiper_value(value)
#    print("Wiper value set to", value)
