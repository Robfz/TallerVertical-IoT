import time
import pyupm_grove as grove
import pyupm_ttp223 as ttp223
import socket
import fcntl
import struct
import pyupm_i2clcd as lcd
import csv
from firebase import Firebase
import time
global url
url = 'https://crackling-torch-3921.firebaseio.com/lots'
global test_plate
test_plate = "ABC-00-00"
global test_entrance
test_entrance = "default"
def startup():
    fire = Firebase(url)
    with open('lot.csv', 'rb+') as csvfile:
       spamreader = csv.reader(csvfile, delimiter=',')
       global lot
       lot = []
       global spots_left
       global spots_max
       spots_left = [0]
       spots_max = [0]
       for row in spamreader:
          fire = fire.child(str(row[0])).child(str(row[1]))
          fire.update({'lot' : int(row[0]), 'spot' : int(row[1]), 'available' : int(row[2])})
          fire = fire.child("visitor_info")
          fire.child("timestamps");
          fire.child("entrance");
          fire.child("plates");
          fire = fire.parent().parent().parent()
          if len(spots_left)-1 < int(row[0]):
             spots_left.append(1)
             spots_max.append(1)
          if int(row[2]) == 1:
             spots_left[int(row[0])] += 1
          spots_max[int(row[0])] += 1
       fire = Firebase(url).child('max')
       for i in range(0, len(spots_left)-1):
          fire = fire.child(str(i+1))
          fire.update({'max' : str(spots_max[i+1]-1)})
          fire = fire.parent()
       fire = fire.parent()
       fire = fire.child('current')
       for i in range(0, len(spots_left)-1):
          fire = fire.child(str(i+1))
          fire.update({'left' : str(spots_left[i+1]-1)})
          fire = fire.parent()


def spaces_available(lot_number):
    return int(Firebase(url).child('current').child(str(lot_number)).get()['left'])


def maximum_spaces(lot_number):
    return int(Firebase(url).child('max').child(str(lot_number)).get()['max'])


def is_available(lot_number, spot):
    info = Firebase(url).child(str(lot_number)).child(str(spot)).get()
    if int(info["available"]) == 1:
       return True
    else:
       return False


def is_busy(lot_number, spot):
    lot_number = int(lot_number)
    spot = int(spot)
    info = Firebase(url).child(str(lot_number)).child(str(spot)).get()
    if int(info["available"]) == 0:
       return True
    else:
       return False


def set_timestamp(lot_number, spot):
    fire = Firebase(url).child(str(lot_number)).child(str(spot)).child("timestamps")
    fire.push({"timestamp":str(time.time())})


def set_entrance(lot_number, spot, entrance):
    fire = Firebase(url).child(str(lot_number)).child(str(spot)).child("entrance")
    fire.push({"entrance":str(entrance)})


def set_plates(lot_number, spot, plates):
    fire = Firebase(url).child(str(lot_number)).child(str(spot)).child("plates")
    fire.push({"plates":str(plates)})


def reserve_available(lot_number, spot):
    lot_number = int(lot_number)
    spot = int(spot)
    fire = Firebase(url).child(str(lot_number)).child(str(spot))
    if is_available(lot_number, spot):
       fire2 = Firebase(url).child('current').child(str(lot_number))
       if(spaces_available(lot_number)>0):
          fire2.update({'left':str(spaces_available(lot_number) - 1)})
          fire.update({'lot' : lot_number, 'spot' : spot, 'available' : 0})
          set_timestamp(lot_number, spot)
          set_plates(lot_number, spot, test_plate)
          set_entrance(lot_number, spot, test_entrance)
          return True
       else:
          return False
    else:
       return False


def release_busy(lot_number, spot):
    fire = Firebase(url).child(str(lot_number)).child(str(spot))
    if is_busy(lot_number, spot):
       fire2 = Firebase(url).child('current').child(str(lot_number))
       left = fire2.get()
       if(spaces_available(lot_number)<= maximum_spaces(lot_number)):
          fire2.update({'left':str(int(left['left']) + 1)})
          fire.update({'lot' : lot_number, 'spot' : spot, 'available' : 1})
          return True
       else:
          return False
    else:
       return False


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



def get_current():
    return Firebase(url).child("current").get


def print_capacities_LCD(myLcd):
    myLcd.clear()
    myLcd.setCursor(0,0)
    fire = get_current()
    zone_1_cap = fire["1"]["left"]
    zone_2_cap = fire["2"]["left"]

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


def print_capacities():
    fire = get_current()
    zone_1_cap = fire["1"]["left"]
    zone_2_cap = fire["2"]["left"]
    print 'Zone 1 capacity: ' + str(zone_1_cap)
    print 'Zone 2 capacity: ' + str(zone_2_cap)


def listen():
    fire = get_current()
    zone_1_cap = fire["1"]["left"]
    zone_2_cap = fire["2"]["left"]
    touch = ttp223.TTP223(3)
    button = grove.GroveButton(4)

    myLcd = prepare_LCD()
    print_capacities()
    print_capacities_LCD(myLcd)
    is_full = False
    i = maximum_spaces(1)
    while (1):
        if button.value() == 1:
            fire = get_current()
            zone_1_cap = fire["1"]["left"]
            zone_2_cap = fire["2"]["left"]
            if zone_1_cap > 0:
                reserve_available(1,i)
                print_capacities()
                print_capacities_LCD(myLcd)

        if touch.isPressed():
            if zone_1_cap < maximum_spaces(1):
                zone_1_cap = zone_1_cap + 1
                print_capacities()
                print_capacities_LCD(myLcd)
                is_full = True


        if zone_1_cap == 0 and zone_2_cap == 0 and is_full:
            print 'Parking full'
            print_text_LCD("Parking Full :(", "Please wait.", myLcd)
            is_full = False

        time.sleep(.5)


def main():
    fire = get_current()
    listen(fire["1"]["left"], fire["2"]["left"])


if __name__ == '__main__':
    main()








