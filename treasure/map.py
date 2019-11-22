import json
from stack import Stack

class Map:
    def __init__(self):
        self.data = {}
        self.length = len(self.data)
        self.load_map()

    
    def load_map(self):
        with open("map.txt") as json_map:
            self.data = json.load(json_map)
        print(self.data)

    def check_room(self, roomId):
        if str(roomId) in self.data:
            return True
        else:
            return False

    def add(self, new_room):
        roomId = new_room['room_id']

        self.data[roomId] = {x:-1 for x in new_room['exits']}

        with open('map.txt', 'w') as outfile:
            json.dump(self.data, outfile)

        self.load_map()

    def update(self, prev_room, new_room, direction):

        opp_dir = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}
        self.data[str(prev_room)][direction] = new_room
        self.data[str(new_room)][direction] = prev_room
