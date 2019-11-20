import requests
import json
import time


class Miner:
    def __init__(self):

        self.opp_dir = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}
        self.encumbered = False
        self.server_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv'
        self.api_key = 'd47e702dfe740c3824f91f1e9fea876009f589c2'
        self.auth_header = {
            'Authorization': f"Token {self.api_key}",
            'Content-Type': 'application/json'
        }
        req_data = self.make_request('init')
        self.current_room = str(req_data['room_id'])
        self.current_room_title = req_data['title']
        self.exits = req_data['exits']
        self.cool_down = req_data['cooldown']

        print(req_data)


    def make_request(self, req_type, data=None):
       
        if data:
            data_json = json.dumps(data)

        if req_type == 'init':
            r = requests.get(self.server_url + '/init/',
                             headers=self.auth_header)
        
        elif req_type == 'move':
            move = {'direction':'n'}
            r = requests.post(self.server_url + '/move/',
                              headers=self.auth_header, json = move)
            print('data: ',data_json)
            print('response: ', r)
        
        else:
            print('wrong req')

        req_data = r.json()

        return req_data

    def explore(self):

        move = {"direction":"n"}
        # move_response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=self.auth_header, json=move)
        # print(move_response)
        # print('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', f'headers={self.auth_header}, json={move}')
        
        
        data = {'direction':'n'}
        self.make_request('move', data)

        # req_data = self.make_request('init')
       

        #print(req_data)

Miner().explore()