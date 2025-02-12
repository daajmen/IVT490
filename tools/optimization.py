import time 

def correction_wiper(wiper_value, heatpump_roomsensor, house_average_temperature): 
    MAX_WIPER = 44
    MIN_WIPER = 39
    TEMP_THRESHOLD = 0.4
   # Högre wiper är högre temp
   
   # Om rumsgivare är högre i värmepumpen
    if (heatpump_roomsensor - house_average_temperature) > TEMP_THRESHOLD: 
        
        # Då sänker temperaturen, öka wiper? 
        new_wiper = wiper_value - 1
        print(f'sänker värdet till {new_wiper}')
        return max(MIN_WIPER, new_wiper)
   # Om rumsgivare är lägre i värmepumpen
    elif (heatpump_roomsensor - house_average_temperature) < -TEMP_THRESHOLD:
        new_wiper = wiper_value + 1
        print(f'ökar värdet till {new_wiper}')
        return min(MAX_WIPER, new_wiper)
      
    return new_wiper


#wiper = 35 
#heatpump_roomsensor = 19
#house_average_temperature = 20.5 
#
#while True: 
#    wiper = correction_wiper(wiper, heatpump_roomsensor, house_average_temperature) 
#    print(f'wiper is now : {wiper}')
#    time.sleep(10)