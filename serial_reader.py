import serial

# Initiera seriell kommunikation
ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)

mappings = {
    1: ("Framledning", 0.1),
    2: ("Ute", 0.1),
    3: ("Tappvarmvatten Topp", 0.1),
    4: ("Varmvatten Mitt", 0.1),
    5: ("Värmevatten Botten", 0.1),
    6: ("Rumstemp", 0.1),
    7: ("Hetgas", 0.1),
    8: ("Extra Acc-Tank", 0.1),
    9: ("Tryckvakt", 1),
    10: ("Högtryck", 1),
    11: ("Lågtryck", 1),
    12: ("Semester aktiv?", 1),
    13: ("Kompressor aktiv", 1),
    14: ("SV1 Öppna", 1),
    15: ("SV1 Stäng", 1),
    16: ("P1 Rad", 1),
    17: ("Fläkt", 1),
    18: ("Larm aktiv", 1),
    19: ("Extern P2", 1),
    20: ("LLT GT1", 0.1),
    21: ("LL GT1", 0.1),
    22: ("BV GT1", 0.1),
    23: ("UL GT1", 0.1),
    24: ("LL GT3:2", 0.1),
    25: ("ULT GT3:2", 0.1),
    26: ("UL GT3:2", 0.1),
    27: ("LL GT3:3", 0.1),
    28: ("BV GT3:3", 0.1),
    29: ("SV3 BV Förskj", 1),
    30: ("Effekt ink vit VV behov", 1),
    31: ("Tillskotstimer VV behov", 1),
    32: ("Tappv prio", 1),
    33: ("Tillskott i %/10", 0.1),
    34: ("Tillskott RAD", 1),
    35: ("Tillskott Tillägg", 1),
    36: ("Default SV2 Open", 1)
}


print("Lyssnar på värmepumpens data...")
try:
    while True:
        raw_data = ser.readline().decode('utf-8').strip()
        if raw_data:
            # Dela upp data i värden
            values = raw_data.split(';')
            
            # Mappa värdena till deras namn och skala
            parsed_data = {}
            for index, (name, scale) in mappings.items():
                if index < len(values):  # Kontrollera att vi inte går utanför datan
                    try:
                        raw_value = int(values[index])
                        parsed_data[name] = raw_value * scale
                    except ValueError:
                        print(f"Ogiltigt värde på index {index}: {values[index]}")
                        parsed_data[name] = None  # Sätt som None om det är ogiltigt

            # Formatera och skriv ut datan
            for name, value in parsed_data.items():
                print(f"{name}: {value}")
            print("-" * 40)  # Separator för att göra det lättare att läsa
except KeyboardInterrupt:
    print("Avslutar...")
finally:
    ser.close()
