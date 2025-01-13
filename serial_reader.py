import serial
from mqtt_handle import data_to_json

# Initiera seriell kommunikation
ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)

mappings = {
    1: ("supply", 0.1),
    2: ("outdoor", 0.1),
    3: ("hotwater_top", 0.1),
    4: ("hotwater_mid", 0.1),
    5: ("hotwater_low", 0.1),
    6: ("roomtemp", 0.1),
    7: ("hotgas", 0.1),
    8: ("extra_tank", 0.1),
    9: ("pressure_sensor", 1),
    10: ("high_pressure", 1),
    11: ("low_pressure", 1),
    12: ("vacation_mode", 1),
    13: ("compressor", 1),
    14: ("open_valve", 1),
    15: ("close_valve", 1),
    16: ("heat_pump", 1),
    17: ("fan", 1),
    18: ("alarm_active", 1),
    19: ("external_pump", 1),
    20: ("llt_gt1", 0.1),
    21: ("ll_gt1", 0.1),
    22: ("setpoint_gt1", 0.1),
    23: ("ul_gt1", 0.1),
    24: ("ll_gt3_2", 0.1),
    25: ("ult_gt3_2", 0.1),
    26: ("ul_gt3_2", 0.1),
    27: ("ll_gt3_3", 0.1),
    28: ("setpoint_gt3_3", 0.1),
    29: ("setpoint_offset_sv3", 1),
    30: ("power_inc_hotwater_demand", 1),
    31: ("boost_timer_hotwater", 1),
    32: ("hotwater_prio", 1),
    33: ("addition", 0.1),
    34: ("addition_rad", 1),
    35: ("addition_supplement", 1),
    36: ("default_sv2_open", 1)
}
def get_data(raw_data): 
    # Dela upp data i värden
    values = raw_data.split(';')
    
    # Mappa värdena till deras namn och skala
    parsed_data = {}
    for index, (name, scale) in mappings.items():
        if index < len(values):  # Kontrollera att vi inte går utanför datan
            try:
                raw_value = int(values[index])
                parsed_data[name] = round(raw_value * scale,1)
            except ValueError:
                print(f"Ogiltigt värde på index {index}: {values[index]}")
                parsed_data[name] = None  # Sätt som None om det är ogiltigt
    # Formatera och skriv ut datan
    #for name, value in parsed_data.items():
    #    print(f"{name}: {value}")
    return parsed_data.items()


try:
    while True:
        raw_data = ser.readline().decode('utf-8').strip()
        if raw_data:
            data = get_data(raw_data)
            print(data_to_json(data))
except KeyboardInterrupt:
    print("Avslutar...")
finally:
    ser.close()
    print("Seriell anslutning stängd.")
