class User:

    def __init__(self, email, schedule, name, plates):
        self.name = name
        self.schedule = schedule
        self.email = email
        self.plates = plates

    def get_name(self):
        return self.name

    def get_schedule(self):
        return self.schedule
