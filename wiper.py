import board
import busio
from adafruit_ds1841 import DS1841


def set_wiper_value(value):
    i2c = busio.I2C(board.SCL, board.SDA)

    ds1841 = DS1841(i2c)
    ds1841.lut_mode_enabled = False

    # Läs wiper-värdet
    ds1841.wiper = value
