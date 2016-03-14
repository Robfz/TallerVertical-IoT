# Author: Roberto Fierros Zepeda

import time
import pyupm_grove as grove
import pyupm_ttp223 as ttp223

def print_capacities(zone_1_cap, zone_2_cap):
    print 'Zone 1 capacity: ' + str(zone_1_cap)
    print 'Zone 2 capacity: ' + str(zone_2_cap)

def listen(zone_1_cap, zone_2_cap):
    touch = ttp223.TTP223(7)
    button = grove.GroveButton(8)
    while (1):
        if button.value() == 1:
            if zone_1_cap > 0:
                zone_1_cap = zone_1_cap - 1
            elif zone_2_cap > 0:
                zone_2_cap = zone_2_cap - 1
            elif zone_1_cap == 0 and zone_2_cap == 0:
                print 'Parking full'
            print_capacities(zone_1_cap, zone_2_cap)
            time.sleep(0.2)

        if touch.isPressed():
            if zone_2_cap == 20:
                zone_1_cap = zone_1_cap + 1
            elif zone_1_cap == 0:
                zone_2_cap = zone_2_cap + 1
            print_capacities(zone_1_cap, zone_2_cap)
            time.sleep(0.2)

def main():
    zone_1_cap = 20
    zone_2_cap = 20

    listen(zone_1_cap, zone_2_cap)

if __name__ == '__main__':
    main()
