import serial

# Initiera seriell kommunikation
ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)

print("Lyssnar på värmepumpens data...")
try:
    while True:
        data = ser.readline().decode('utf-8').strip()
        if data:
            print(f"Mottaget: {data}")
except KeyboardInterrupt:
    print("Avslutar...")
finally:
    ser.close()
