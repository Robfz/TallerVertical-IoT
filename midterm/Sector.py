class Sector:

    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon

    def get_lat(self):
        return self.lat

    def get_lon(self):
        return self.lon

    def get_name(self):
        return self.name
