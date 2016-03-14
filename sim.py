# Author: Roberto Fierros Zepeda

import time
import pyupm_grove as grove
import pyupm_ttp223 as ttp223

def listen(zone_1_cap, zone_2_cap):
    touch = ttp223.TTP223(7)
    button = grove.GroveButton(8)
    while (1):
        if touch.isPressed():
            print touch.name(), 'is pressed'
        else:
            print touch.name(), 'is not pressed'
        print button.name(), ' value is ', button.value()
        time.sleep(0.05)

def main():
    zone_1_cap = 20
    zone_2_cap = 20

    listen(zone_1_cap, zone_2_cap)

if __name__ == '__main__':
    main()
