class User:

    def __init__(self, name, schedule):
        self.name = name
        self.schedule = schedule

    def get_name(self):
        return self.name

    def get_schedule(self):
        return self.schedule
