import Queue
import Zone
import User
import Sector
import math
from firebase import firebase

database = firebase.FirebaseApplication('https://spot2016.firebaseio.com', None)


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
        user_name = result['name']
        user_pref = result['horario']['Monday']
        users.append(User.User(user_name, user_pref))

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
    database.put('/zones', zone.get_name(),
                 {'current_cap': zone.get_current_cap() + 1,
                  'max_cap': zone.get_max_cap(),
                  'name': zone.get_name(),
                  'position': {
                       'lat': zone.get_lat(),
                       'lon': zone.get_lon()
                    }
                  })


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


def main():

    populate_db()

    users = get_users()
    sectors = get_sectors()

    for user in users:
        zones = build_zones()
        suggest(zones, sectors, user)


if __name__ == '__main__':
    main()
