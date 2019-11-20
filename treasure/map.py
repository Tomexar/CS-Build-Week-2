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
        print('map loaded')

    def check_room(self):
        if str(roomId)

    def add(self):


Map()