# Author: Roberto Fierros Zepeda

import time
import pyupm_grove as grove
import pyupm_ttp223 as ttp223
import socket
import fcntl
import struct
import thread

import pyupm_i2clcd as lcd
import sys

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
	if(zone_1_cap != 0 and zone_2_cap != 0):
		myLcd.clear()
		myLcd.setCursor(0,0)
		myLcd.write("Zone 1: " + str(zone_1_cap) + " SPOTS.")
		myLcd.setCursor(1,0)
		myLcd.write("Zone 2: " + str(zone_2_cap) + " SPOTS.")

def print_text_LCD(string, string2, myLcd):
	myLcd.clear()
	myLcd.setCursor(0,0)
	myLcd.write(string)
	myLcd.setCursor(1,0)
	myLcd.write(string2)
	


def print_capacities(zone_1_cap, zone_2_cap):
	print 'Zone 1 capacity: ' + str(zone_1_cap)
	print 'Zone 2 capacity: ' + str(zone_2_cap)

def listen(zone_cap,button,touch,myLcd):
	while(1):
		if button.value() == 1:
			if zone_cap > 0:
				zone_cap = zone_cap - 1
		elif touch.isPressed():
			if zone_cap < 20:
				zone_cap = zone_cap + 1
		print_capacities_LCD(zone_1_cap,zone_2_cap,myLcd)
		time.sleep(.5)
		return zone_cap
def check_full(zone_1_cap,zone_2_cap,myLcd):
	while(1):
		if(zone_1_cap == zone_2_cap and zone_1_cap == 0):
			print_text_LCD("Parking full.","Please wait :)",myLcd)
		time.sleep(.5)
def main():
	touch = ttp223.TTP223(3)
	button = grove.GroveButton(4)
	button2 = grove.GroveButton(8)
	touch2 = ttp223.TTP223(7)
	myLcd = prepare_LCD()
	zone_1_cap = 20
	zone_2_cap = 20
	zone_1_cap = thread.start_new_thread( listen, (zone_1_cap, button, touch, myLcd ) )
	zone_2_cap = thread.start_new_thread( listen, (zone_2_cap, button2, touch,myLcd) )
	while(1):
		check_full(zone_1_cap,zone_2_cap,myLcd)
if __name__ == '__main__':
	main()
