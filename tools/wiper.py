import board
import busio
from adafruit_ds1841 import DS1841


def set_wiper_value(value):
    i2c = busio.I2C(board.SCL, board.SDA)

    ds1841 = DS1841(i2c)
    ds1841.lut_mode_enabled = False

    # Läs wiper-värdet
    ds1841.wiper = value


# Funktion för att hantera wiper-värden
def handle_wiper(input_value):
    # 39 := 20.6    # 40 := 21.1    # 41 := 21.9    # 42 := 21.9    # 43 := 22.0??
    try:
        set_wiper_value(input_value)
        print("Wiper value set to", input_value)
    except ValueError:
        print("Ogiltigt värde! Ange ett tal mellan 0 och 127.")
