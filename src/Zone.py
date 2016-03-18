class Zone:

    def __init__(self, zone_name, max_cap, current_cap, lat, lon):
        self.max_cap = max_cap
        self.current_cap = current_cap
        self.zone_name = zone_name
        self.lat = lat
        self.lon = lon

    def get_name(self):
        return self.zone_name

    def car_in(self):
        if self.max_cap == self.current_cap:
            return False
        self.current_cap += 1
        return True

    def is_empty(self):
        return self.current_cap == 0

    def is_full(self):
        return self.current_cap == self.max_cap

    def get_occupation(self):
        return float(self.current_cap) / self.max_cap

    def get_lon(self):
        return self.lon

    def get_lat(self):
        return self.lat

    def get_current_cap(self):
        return self.current_cap

    def get_max_cap(self):
        return self.max_cap
