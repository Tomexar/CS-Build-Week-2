import requests
import json
import time
import random
import hashlib
from map import Map
from stack import Stack
from timeit import default_timer as timer


class Miner:
    def __init__(self):

        self.opp_direction = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}
        self.encumbered = False
        self.server_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv'
        self.api_key = 'd47e702dfe740c3824f91f1e9fea876009f589c2'
        self.auth_header = {
            'Authorization': f"Token {self.api_key}",
            'Content-Type': 'application/json'
        }

        self.data = {}
        self.name = ''
        self.encumbered = False 
        self.encumbrance = 0
        self.str = 0
        self.spd = 0
        self.inv = []
        self.current_room = ''
        self.cooldown = 0
        self.gold = 0 
        self.current_room_title = ''
        self.exits = []
        self.coordinates = []
        self.messages = []
        self.mine = '143'

        map_graph = {}
        with open('map.json', mode = 'r') as m:
            map_graph = json.loads(m.read().strip())
            print("map loaded")
            #print(map_graph)

            self.new_map = {**map_graph}
            #print('new map', self.new_map)

            #print('len', len(self.new_map.keys()))
        
        data = self.init()
        self.data = self.new_map
        print(data)


    def make_request(self, req_type, data=None):
       
        if data:
            data_json = json.dumps(data)

        if req_type == 'init':
            r = requests.get(self.server_url + '/init/',
                             headers=self.auth_header)
        
        elif req_type == 'move':

            r = requests.post(self.server_url + '/move/',
                              headers=self.auth_header, data = data_json)
        
        elif req_type == 'status':
            r = requests.post(self.server_url + '/status/',
                              headers=self.auth_header)

        elif req_type == 'take':
            r = requests.post(self.server_url + '/take/',
                              headers=self.auth_header, data=data_json)
        
        else:
            print('wrong req')

        req_data = r.json()

        cooldown = req_data['cooldown']
        print(f'CD: {cooldown}')
        while cooldown > 0:
            if(cooldown > 1):
                time.sleep(1)
                cooldown -= 1
            else:
                time.sleep(cooldown)
                cooldown = 0

        return req_data

    def map(self, res_data, direction):

        previous = self.current_room
        reverse_direction = self.opp_direction[direction]
        self.exits = res_data['exits']
        self.cooldown = res_data['cooldown']

        if self.current_room not in self.new_map:
            found_exits = {}
            for exit_direction in self.exits:
                found_exits[exit_direction] = '?'
            self.new_map[self.current_room] = {
                'exits': found_exits
            }

        if len(self.new_map.keys()) < 499:
            self.new_map[previous]['exits'][direction] = self.current_room
            self.new_map[self.current_room]['exits'][reverse_direction] = previous
        
        self.update_map()

    
    def update_map(self):
        with open ('map.json', mode = 'w') as m:
            json.dump(self.new_map, m )
        #print('new map', self.new_map)
        self.data = self.new_map


    def init(self):
        response = self.make_request('init')
        data = response
        self.current_room = data['room_id']
        self.current_room_title = data['title']
        self.cooldown = data['cooldown']
        self.exits = data['exits']
        self.coordinates = data['coordinates']
        #print(data)
        return data

    def status(self):
        response = self.make_request('status')
        data = response
        print(data)

        self.name = data['name']
        self.encumbrance = data['encumbrance']
        self.str = data['strength']
        self.spd = data['speed']
        self.gold = data['gold']
        self.messages = data['messages']
        self.inv = data['inventory']

        return data


    def find_path(self, start_room, end_room):
        visited = []
        stack = Stack()
        stack.push([start_room])

        while stack.size() > 0:
            shortest = stack.pop()
            vertex = shortest[-1]
            if vertex not in visited:
                print(f'{vertex} and {end_room}')
                if vertex == end_room:
                    return shortest
                visited.append(vertex)
                for key, value in self.data[str(vertex)].items():
                    new_shortest = list(shortest)
                    new_shortest.append(value)
                    stack.push(new_shortest)

        return None

    def make_path(self, destination):
        time.sleep(self.cooldown + 1)
        path = self.find_path(self.current_room, destination)

    def find_direction(self, room_id, next_id):
        for key, value in self.data[str(room_id)].items():
            if value == next_id:
                return key

    def know_id(self, roomId, direction):
        if self.data[str(roomId)][direction] != '?':
            return str(self.data[str(roomId)][direction])
        return False

    def travel(self, direction):
        print('traveling ', direction)

        if direction == 'n':
            json = {"direction":"n"}
            if self.know_id(self.current_room, direction):
                json['next_room_id'] = self.know_id(self.current_room, direction)
            response = requests.post(self.server_url + '/move/', headers = self.auth_header, json = json)
            data = response.json()
            return data

        if direction == 's':
            json = {"direction":"s"}
            if self.know_id(self.current_room, direction):
                json['next_room_id'] = self.know_id(self.current_room, direction)
            response = requests.post(self.server_url + '/move/', headers = self.auth_header, json = json)
            data = response.json()
            return data
        
        if direction == 'e':
            json = {"direction":"e"}
            if self.know_id(self.current_room, direction):
                json['next_room_id'] = self.know_id(self.current_room, direction)
            response = requests.post(self.server_url + '/move/', headers = self.auth_header, json = json)
            data = response.json()
            # print(data)
            return data

        if direction == 'w':
            json = {"direction":"w"}
            if self.know_id(self.current_room, direction):
                json['next_room_id'] = self.know_id(self.current_room, direction)
            response = requests.post(self.server_url + '/move/', headers = self.auth_header, json = json)
            data = response.json()
            return data

    def change_name(self):
        json = {"name": "TOM", "confirm":"aye"}
        time.sleep(self.cooldown + 1)
        response = requests.post(self.server_url + '/change_name/', headers = self.auth_header, json = json)
        data = response
        print(data)
        print(data.text)

    def pray(self):
        #SHRINES : 22, 
        #well : 55
        time.sleep(self.cooldown + 1)
        response = requests.post(self.server_url + '/pray/', headers = self.auth_header)
        data  = response
        print(data)
        print(response.text)

    def examine(self):
        json = {"name":'wishing well'}
        time.sleep(self.cooldown)
        response= requests.post(self.server_url + "/examine/", headers = self.auth_header, json = json)
        data = response.json()
        print(data)

        with open('hint.txt', 'w') as outfile:
            outfile.write(data['description'][39:])
            outfile.close()
            ##143

    def proof_of_work(self, last, diff):

        start = timer()
        print('searching')
        proof = 0
        attempts = 0

        while self.valid_proof(last, proof, diff) is False:
            proof = random.randint(0, 950000000)
            attempts += 1
            if attempts >= 8000000:
                print('no')
                return ''
        print('proof: ', proof , 'in: ', attempts)

        return proof

    def valid_proof(self, last, proof, diff):

        guess = f'{last}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        if diff is not None:
            leading_zeros = "0" * diff
        else:
            leading_zeros = "0" * 6

        return guess_hash[0:diff] == leading_zeros


    def mining(self):
        new_proof = ''
        response = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/', headers = self.auth_header)
        data = response.json()
        print(response.text)
        print('proof ', data['proof'], 'diff ', data['difficulty'])
        print(data['proof'], data['difficulty'])
        new_proof = self.proof_of_work(data['proof'], data['difficulty'])

        if new_proof != '':
            json = {'proof': new_proof}
            res = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/bc/mine', headers = self.auth_header, json = json)

            data = res.json()

        time.sleep(self.cooldown)
        print(data)
        
    def get_balance(self):
        headers  = {
            'Authorization': f"Token {self.api_key}",
            'Content-Type': 'application/json'
        }
        response = requests.get( 'https://lambda-treasure-hunt.herokuapp.com/api/bc/get_balance/', headers = self.auth_header)
        print(response.text)
        



    def explore(self):

        # self.travel_to()
        self.status()
        # self.sell()
        #self.change_name()
        # self.pray()
        # self.examine()
        #print('mine', self.mine)
        #self.mining()
        self.get_balance()


        # path = self.find_path(self.current_room, 143)
        # path.pop(0)
        # print(path)
        # for room_id in path:
        #     direction = self.find_direction(self.current_room, room_id)
        #     time.sleep(self.cooldown +1)
        #     new_room = self.travel(direction)
        #     print(new_room)
        #     self.cooldown = new_room['cooldown']
        #     self.current_room = new_room['room_id']

        #print(self.inv)

        # json = {"direction":"e"}
        # response = requests.post(self.server_url + '/move/', headers = self.auth_header, json = json)
        # data = response
        # print(data)
        # print('hello')


        #r = requests.post(self.server_url + '/move/', headers=self.auth_header, data = data_json)

        # data = {'direction':"s"}
        # r_data = self.make_request('move', data)
        # print(r_data)

        # time.sleep(self.cooldown + 1)
        # room_id = self.current_room
        # print(room_id)
        # print(self.data[f"{room_id}"])


        # for exits in self.data[f'{room_id}']['exits']:
        #     print('**')
        #     exit_dir = self.data[f'{room_id}']['exits'][exits]
        #     print(exit_dir)


        # # while len(self.new_map) < 499:
        # #     if self.data[str(room_id)][direction] != '?':
        # #         josn = {'direction':}



    def travel_to(self):
        while True:
            if not self.encumbered:
                path = self.find_path(self.current_room, random.randint(2,499))
                path.pop(0)
                print(path)
                for room_id in path:
                    direction = self.find_direction(self.current_room, room_id)
                    time.sleep(self.cooldown +1)
                    new_room = self.travel(direction)
                    print(new_room)
                    self.cooldown = new_room['cooldown']
                    self.current_room = new_room['room_id']
                    for item in new_room['items']:
                        time.sleep(self.cooldown + 1)
                        json = {"name": item}
                        response = requests.post(self.server_url + '/take/', headers = self.auth_header, json = json)
                        data = response.json()
                        self.cooldown = data['cooldown']
                    time.sleep(self.cooldown + 1)
                    self.status()
                    if not self.encumbered and "Heavily Encumbered: +100% CD" in r_data['messages']:
                        self.encumbered = True
            else:
                path = self.find_path(self.current_room, 1)
                path.pop(0)
                print('going to shop',path)
                for room_id in path:
                    direction = self.find_direction(self.current_room, room_id)
                    time.sleep(self.cooldown + 1)
                    new_room = self.travel(direction)
                    self.cooldown = new_room['cooldown']
                    self.current_room = new_room['room_id']
                
                for item in self.inv:
                    time.sleep(self.cooldown + 1)
                    json = {"name": item}
                    response = requests.post(self.server_url + '/sell/', headers = self.auth_header, json = json)
                    data = response.json()
                    self.cooldown = data['cooldown']
                    time.sleep(self.cooldown + 1)
                    self.status()
                    print('gold: ', self.gold)

    def sell(self):
        for item in self.inv:
            time.sleep(self.cooldown + 1)
            json = {"name": item, "confirm":"yes"}
            print(json)
            response = requests.post(self.server_url + '/sell/', headers = self.auth_header, json = json)
            data = response.json()
            print(data)
            self.cooldown = data['cooldown']
            time.sleep(self.cooldown + 1)
            self.status()
            print('gold: ', self.gold)
    

Miner().explore()