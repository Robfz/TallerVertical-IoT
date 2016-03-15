# Author: Roberto Fierros Zepeda

import time
import pyupm_grove as grove
import pyupm_ttp223 as ttp223
import socket
import fcntl
import struct

import pyupm_i2clcd as lcd


def prepare_LCD():
	# Initialize Jhd1313m1 at 0x3E (LCD_ADDRESS) and 0x62 (RGB_ADDRESS)
	myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)
	# Clear
	myLcd.clear()
	# Green
	myLcd.setColor(255, 255, 0)
	# Zero the cursor
	myLcd.setCursor(0,0)
	return myLcd

def print_capacities_LCD(zone_1_cap, zone_2_cap, myLcd):
	myLcd.clear()
	myLcd.setCursor(0,0)
	if(zone_1_cap <= 9 and zone_2_cap <= 9):
		myLcd.write("Zone 1: 0" + str(zone_1_cap) + " SPOTS")
		myLcd.setCursor(1,0)
		myLcd.write("Zone 2: 0" + str(zone_2_cap) + " SPOTS")
	elif(zone_1_cap > 9 and zone_2_cap <= 9):
		myLcd.write("Zone 1: " + str(zone_1_cap) + " SPOTS")
		myLcd.setCursor(1,0)
		myLcd.write("Zone 2: 0" + str(zone_2_cap) + " SPOTS")

	elif(zone_1_cap <= 9 and zone_2_cap > 9):
		myLcd.write("Zone 1: 0" + str(zone_1_cap) + " SPOTS")
		myLcd.setCursor(1,0)
		myLcd.write("Zone 2: " + str(zone_2_cap) + " SPOTS")
	elif(zone_1_cap > 9 and zone_2_cap > 9):
		myLcd.write("Zone 1: " + str(zone_1_cap) + " SPOTS")
		myLcd.setCursor(1,0)
		myLcd.write("Zone 2: " + str(zone_2_cap) + " SPOTS")

def print_text_LCD(string, string2, myLcd):
	myLcd.clear()
	myLcd.setCursor(0,0)
	myLcd.write(string)
	myLcd.setCursor(1,0)
	myLcd.write(string2)



def print_capacities(zone_1_cap, zone_2_cap):
	print 'Zone 1 capacity: ' + str(zone_1_cap)
	print 'Zone 2 capacity: ' + str(zone_2_cap)

def listen(zone_1_cap, zone_2_cap):
	touch = ttp223.TTP223(3)
	button = grove.GroveButton(4)
	button2 = grove.GroveButton(8)
	touch2 = ttp223.TTP223(7)

	myLcd = prepare_LCD()
	print_capacities(zone_1_cap, zone_2_cap)
	print_capacities_LCD(zone_1_cap, zone_2_cap, myLcd)
	is_full = False
	while (1):
		if button.value() == 1:
			if zone_1_cap > 0:
				zone_1_cap = zone_1_cap - 1
				print_capacities(zone_1_cap, zone_2_cap)
				print_capacities_LCD(zone_1_cap, zone_2_cap, myLcd)
				is_full = True
		if button2.value() == 1:
			if zone_2_cap > 0 :
				zone_2_cap = zone_2_cap - 1
				print_capacities(zone_1_cap, zone_2_cap)
				print_capacities_LCD(zone_1_cap, zone_2_cap, myLcd)
				is_full = True

		if touch.isPressed():
			if zone_1_cap < 20:
				zone_1_cap = zone_1_cap + 1
				print_capacities(zone_1_cap, zone_2_cap)
				print_capacities_LCD(zone_1_cap, zone_2_cap, myLcd)
				is_full = True
		if touch2.isPressed():
			if zone_2_cap < 20:
				zone_2_cap = zone_2_cap + 1
				print_capacities(zone_1_cap, zone_2_cap)
				print_capacities_LCD(zone_1_cap, zone_2_cap, myLcd)
				is_full = True


		if zone_1_cap == 0 and zone_2_cap == 0 and is_full:
			print 'Parking full'
			print_text_LCD("Parking Full :(", "Please wait.", myLcd)
			is_full = False

		time.sleep(.5)
def main():
	zone_1_cap = 20
	zone_2_cap = 20

	listen(zone_1_cap, zone_2_cap)


if __name__ == '__main__':
	main()