import serial

# Initiera seriell kommunikation
ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)

mappings = {
    0: ("Framledning", 0.1),
    1: ("Ute", 0.1),
    2: ("Tappvarmvatten Topp", 0.1),
    3: ("Varmvatten Mitt", 0.1),
    4: ("Värmevatten Botten", 0.1),
    5: ("Rumstemp", 0.1),
    6: ("Hetgas", 0.1),
    7: ("Extra Acc-Tank", 0.1),
    8: ("Tryckvakt", 1),
    9: ("Högtryck", 1),
    10: ("Lågtryck", 1),
    11: ("Semester aktiv?", 1),
    12: ("Kompressor aktiv", 1),
    13: ("SV1 Öppna", 1),
    14: ("SV1 Stäng", 1),
    15: ("P1 Rad", 1),
    16: ("Fläkt", 1),
    17: ("Larm aktiv", 1),
    18: ("Extern P2", 1),
    19: ("LLT GT1", 0.1),
    20: ("LL GT1", 0.1),
    21: ("BV GT1", 0.1),
    22: ("UL GT1", 0.1),
    23: ("LL GT3:2", 0.1),
    24: ("ULT GT3:2", 0.1),
    25: ("UL GT3:2", 0.1),
    26: ("LL GT3:3", 0.1),
    27: ("BV GT3:3", 0.1),
    28: ("SV3 BV Förskj", 1),
    29: ("Effekt ink vit VV behov", 1),
    30: ("Tillskotstimer VV behov", 1),
    31: ("Tappv prio", 1),
    32: ("Tillskott i %/10", 0.1),
    33: ("Tillskott RAD", 1),
    34: ("Tillskott Tillägg", 1),
    35: ("Default SV2 Open", 1)
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
