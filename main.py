import board
import busio
from adafruit_ds1841 import DS1841

# Initiera I2C-bussen
i2c = busio.I2C(board.SCL, board.SDA)

# Skapa en DS1841-instans
ds1841 = DS1841(i2c)

# Stäng av Lookup Table (LUT) om den är aktiv
ds1841.lut_mode_enabled = False
print("LUT-läge avstängt")

# Ställ in wiper-värdet (0–127)
ds1841.wiper = 127

# Läs wiper-värdet
current_value = ds1841.wiper
print(f"Aktuellt wiper-värde: {current_value}")


while True: 

    inputvalue = input("Ange wiper-värde (0–127): ")
    if inputvalue == 'exit':
        break 
    else: 
        ds1841.wiper = int(inputvalue)

    print(f"Wiper inställt till: {ds1841.wiper}")