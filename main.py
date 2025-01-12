from wiper import set_wiper_value

while True:
    value = int(input("Enter a value between 0 and 127: "))
    set_wiper_value(value)
    print("Wiper value set to", value)