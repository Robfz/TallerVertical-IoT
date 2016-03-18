import csv
import Zone

from firebase import firebase

database = firebase.FirebaseApplication('https://spot2016.firebaseio.com', None)


def upload_zones(zones):
    for zone in zones:
        database.put('/zones', zone.get_name(),
                     {'max_cap': zone.get_max_cap(),
                      'current_cap': zone.get_current_cap(),
                      'name': 'Zone ' + zone.get_name(),
                      'position': {'lat': 0, 'lon': 0}
                      })


def build_zones():
    zones = dict()
    with open('init.csv', 'rb') as data:
        reader = csv.reader(data)
        for row in reader:
            if row[0] in zones:
                zones[row[0]] += 1
            else:
                zones[row[0]] = 1
        for zone in zones:
            print zone + " " + str(zones[zone])

    print ""

    occupations = dict()
    with open('init.csv', 'rb') as data:
        reader = csv.reader(data)
        for row in reader:
            if row[2] == '1':
                if row[0] in occupations:
                    occupations[row[0]] += 1
                else:
                    occupations[row[0]] = 1
        for zone in occupations:
            print zone + " " + str(occupations[zone])

    constructed = list()
    for zone in zones:
        constructed.append(Zone.Zone(zone, zones[zone], occupations[zone], 0, 0))
    upload_zones(constructed)


def main():
    build_zones()


if __name__ == '__main__':
    main()