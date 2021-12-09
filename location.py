class Location(object):
    def __init__(self,
                 place: str):

        self.place = place
        self.directions = {}

    def add_direction(self, place: str, distance: int):
        self.directions[place] = distance


class Map(object):
    def __init__(self):
        self.locations = {}
        self.count = 0

    def add_location(self, place: str, location: Location):
        self.locations[place] = location



