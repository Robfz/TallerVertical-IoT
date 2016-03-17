import Queue
import Zone
import User
import Sector
import math
import time
import signal

from firebase import firebase

database = firebase.FirebaseApplication('https://spot2016.firebaseio.com', None)

listen = 1

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
        user_pref = result['horario']['Monday']
        user_plates = result['placas']
        users.append(User.User(user_email, user_pref, user_name, user_plates))

    return users


def get_sectors():
    sectors = list()
    db_result = database.get('/sectors', None)
    for result in db_result:
        lat = result['position']['lat']
        lon = result['position']['long']
        sectors.append(Sector.Sector(result['name'], lat, lon))
    return sectors


def update_zone(zone):
    database.patch('/zones/' + zone.get_name(),
                   {'current_cap': zone.get_current_cap() + 1})


def get_user_pref_sector(user, sectors):
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


def dispatch_job(job):
    user_name = job
    user_json = database.get('/usuarios/' + user_name, None)
    user = User.User(user_json['email'], user_json['horario']['Monday'],
                     user_json['name'], user_json['placas'])
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
    print "User " + user.get_name() + " goes to: " + suggested_zone.get_name()
    print "with score = " + str(user_score(suggested_zone, sector))
    update_zone(suggested_zone)

    return  suggested_zone


def main():
    signal.signal(signal.SIGINT, sigint_handler)

    populate_db()

    sectors = get_sectors()
    zones = build_zones()

    while listen:
        print "Listening for jobs..."
        jobs = database.get('/jobs', None)
        if jobs is None:
            time.sleep(1.0)
            continue
        for job in jobs:
            if jobs[job] != 'true':
                continue
            suggested = suggest(zones, sectors, dispatch_job(job))
            database.put('/jobs', job, suggested.get_name())
        time.sleep(1.0)


if __name__ == '__main__':
    main()
