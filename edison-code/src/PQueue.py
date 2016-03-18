import Queue
import Zone
import User
import Sector
import math
import time
import datetime
import signal

import pyupm_i2clcd as lcd
import pyupm_grove as grove
import pyupm_ttp223 as ttp223

from firebase import firebase

database = firebase.FirebaseApplication('https://spot2016.firebaseio.com', None)
LCD = lcd.Jhd1313m1(0, 0x3E, 0x62)
listen = 1
day = 'Monday'


def get_day():
    global day
    day = datetime.datetime.today().weekday()
    if day == 0:
        day = 'Monday'
    elif day == 1:
        day = 'Tuesday'
    elif day == 2:
        day = 'Wednesday'
    elif day == 3:
        day = 'Thursday'
    elif day == 4:
        day = 'Friday'
    elif day == 5:
        day = 'Saturday'

def sigint_handler(signum, frame):
    print('SIGINT caught, exiting gracefully...')
    global listen
    listen = 0


def populate_db():
    database.put('/zones', 'Zona 1',
                 {'current_cap': 0,
                  'max_cap': 20,
                  'name': 'Zona 1',
                  'position': {
                       'lat': 5,
                       'lon': 5
                  }
                  })

    database.put('/zones', 'Zona 2',
                 {'current_cap': 0,
                  'max_cap': 20,
                  'name': 'Zona 2',
                  'position': {
                       'lat': -5,
                       'lon': 5
                  }
                  })


def build_zones():
    zones = list()
    db_result = database.get('/zones', None)
    for result in db_result:
        result = db_result[result]
        lat = result['position']['lat']
        lon = result['position']['lon']
        zones.append(Zone.Zone(result['name'], result['max_cap'], result['current_cap'], lat, lon))

    return zones


def get_users():
    users = list()
    db_result = database.get('/usuarios', None)
    for result in db_result:
        result = db_result[result]
        user_email = result['email']
        user_name = result['name']
        user_pref = result['schedule']['Monday']
        user_plates = result['plates']
        users.append(User.User(user_email, user_pref, user_name, user_plates))

    return users


def get_sectors():
    sectors = list()
    db_result = database.get('/sectors', None)
    for result in db_result:
        lat = result['position']['lat']
        lon = result['position']['lon']
        sectors.append(Sector.Sector(result['name'], lat, lon))
    return sectors


def update_zone(zone):
    database.patch('/zones/' + zone.get_name(),
                   {'current_cap': zone.get_current_cap() + 1})


def release_spot_zone(zone):
    print str(zone.get_current_cap())
    print str(zone.get_current_cap() - 1)
    database.patch('/zones/' + zone.get_name(),
                   {'current_cap': zone.get_current_cap() - 1})


def get_user_pref_sector(user, sectors):
    if user is None:
        return None
    sector_interest = None
    for sector in sectors:
        if sector.get_name() == user.get_schedule():
            sector_interest = sector
    return sector_interest


def user_score(zone, sector):
    if zone.is_full():
        return float('inf')
    if sector is None:
        return zone.get_occupation()

    term1 = math.pow(sector.get_lon() - zone.get_lon(), 2)
    term2 = math.pow(sector.get_lat() - zone.get_lat(), 2)
    distance = math.sqrt(term1 + term2)
    return distance


def get_user(job):
    user_name = job
    user_json = database.get('/usuarios/' + user_name, None)
    user = User.User(user_json['email'], user_json['schedule']['Monday'],
                     user_json['name'], user_json['plates'])
    return user


def suggest(zones, sectors, user):
    pqueue = Queue.PriorityQueue()

    # Get user preferred zone
    sector = get_user_pref_sector(user, sectors)
    if sector is None:
        print "No user preference found"
    else:
        print "User preferred sector: " + sector.get_name()

    for zone in zones:
        pqueue.put((zone.get_occupation() + user_score(zone, sector), zone))

    suggested_zone = pqueue.get()[1]
    if user is None:
        print "Unknown user dispatched"
    else:
        print "User " + user.get_name() + " goes to: " + suggested_zone.get_name()
        print "with score = " + str(user_score(suggested_zone, sector))
    update_zone(suggested_zone)

    return  suggested_zone


def print_stop_sign():
    LCD.setColor(255, 0, 0)
    LCD.setCursor(0,0)
    LCD.write("Spot park service")
    LCD.setCursor(1,0)
    LCD.write("                 ")


def print_suggested_zone(suggested_zone):
    LCD.setCursor(1,0)
    LCD.setColor(0, 255, 0)
    LCD.write(("Go to  " + suggested_zone.get_name()).encode('utf-8'))


def dispatch_app_job(jobs, zones, sectors):
    if jobs is None:
        time.sleep(0.5)
        return
    for job in jobs:
        if jobs[job] != 'true':
            continue
        suggested = suggest(zones, sectors, get_user(job))
        print_suggested_zone(suggested)
        database.put('/jobs', job, 'Zone ' + suggested.get_name())
    time.sleep(1.0)


def dispatch_button(zones, sectors):
    suggested = suggest(zones, sectors, None)
    print 'Local job dispatched: in'
    print 'Go to Zone ' + suggested.get_name()
    print_suggested_zone(suggested)
    time.sleep(1.0)


def dispatch_touch(zones, sectors):
    print 'Local job dispatched: out'
    release_spot_zone(zones[0])
    print 'Released spot from Zone ' + zones[0].get_name()
    time.sleep(1.0)


def main():
    signal.signal(signal.SIGINT, sigint_handler)
    button = grove.GroveButton(4)
    touch = ttp223.TTP223(3)

    sectors = get_sectors()
    zones = build_zones()
    get_day()
    print day

    LCD.setCursor(0,0)
    LCD.setColor(255, 0, 0)

    while listen:
        print "Listening for jobs..."
        print_stop_sign()

        zones = build_zones()

        if button.value() == 1:
            dispatch_button(zones, sectors)
            continue

        if touch.isPressed():
            dispatch_touch(zones, sectors)
            continue

        jobs = database.get('/jobs', None)
        dispatch_app_job(jobs, zones, sectors)


if __name__ == '__main__':
    main()
