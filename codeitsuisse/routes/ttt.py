import logging
import json
import requests
import time
import random

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

def calc_move(position, chara):
    move = {}
    plist = ['NW', 'N', 'NE', 'W', 'C', 'E', 'SW', 'S', 'SE']
    for i in position:
        if i in plist:
            plist.remove(i)
    move['player'] = chara
    move['action'] = 'putSymbol'
    move['position'] = random.choice(plist)
    return move

@app.route('/tic-tac-toe', methods=['POST'])
def getid():
    data = request.get_json()
    logging.info('data sent for getid {}'.format(data))
    battleId = data.get('battleId')
    logging.info('battleId :{}'.format(battleId))
    # print(battleId)
    start_url = 'https://cis2021-arena.herokuapp.com/tic-tac-toe/start/{}'.format(battleId)
    play_url = 'https://cis2021-arena.herokuapp.com/tic-tac-toe/play/{}'.format(battleId)

    for i in range(9):
        position = dict()
        r = requests.get(start_url)
        # a = requests.get('https://cis2021-arena.herokuapp.com/tic-tac-toe/start/acwcwcwc') # for test connection
        message = r.json()
        logging.info('data get for message {}'.format(r))
        try:
            chara = message['youAre']
        except: pass

        time.sleep(2)
        try:
            if message['action'] == 'putSymbol':
                position[(message['position'])]=message['player']
        except: pass
        move = calc_move(position, chara = '0')
        logging.info('the move is {}'.format(move))
        requests.post(play_url, data = move)



    return json.dumps(battleId)
'''
|NW|N |NE|
+--+--+--+
|W |C |E |
+--+--+--+
|SW|S |SE|
{
  "action": "putSymbol",
  "position": "SE"
}
'''

@app.route('/tic-tac-toe/<battleId>', methods=['POST'])
def id(battleId):
    id = getid()
    return battleId
def chess():
    data = request.get_json()
    logging.info('data sent for chess {}'.format(data))
    action = data.get('action')
    position = data.get('position')
    return json.dumps(action, position)
