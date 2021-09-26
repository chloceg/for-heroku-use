import logging
import json
from flask.sessions import SessionInterface
import requests

from flask import request
import sseclient

from flask import Flask, render_template, jsonify
from werkzeug.exceptions import RequestTimeout
from codeitsuisse import app;
from random import choice

logger = logging.getLogger(__name__)


# Edit route
@app.route('/tic-tac-toe', methods=['POST'])
# De-conflict function names
def ttt_submission():
    data = request.get_json()
    logging.info("Data received from evaluation: {}".format(data))
    battleId = data.get("battleId")
    # logging.info("BattleID: {}".format(battleId))

    url = f'https://cis2021-arena.herokuapp.com/tic-tac-toe/start/{battleId}'
    post_url = f'https://cis2021-arena.herokuapp.com/tic-tac-toe/play/{battleId}'

    response = with_requests(url)  # or with_requests(url)
    client = sseclient.SSEClient(response)

    young_god = None
    positions = {'NW': (0, 0), 'N': (0, 1), 'NE': (0, 2), 'W': (1, 0), 'C': (1, 1), 'E': (1, 2), 'SW': (2, 0),
                 'S': (2, 1), 'SE': (2, 2)}
    seen = set(positions.keys())

    for event in client.events():
        data = json.loads(event.data)
        logging.info(f'New event: {data}')

        # Initialize (I start)
        if not young_god and 'youAre' in data:
            young_god = data['youAre']
            logging.info(f'Response: Setting player to... is {young_god}, taking center pos')
            requests.post(post_url, json={"action": "putSymbol", "position": "C"})
            seen.remove("C")
            continue

        if 'action' in data and data["player"] != young_god:
            # fill the board then send a respond
            if data['action'] == 'putSymbol':
                logging.info(f'Response: Opponent is {data["player"]}, taking {data["position"]}')
                if data['position'] not in seen:
                    flip = "(╯°□°)╯︵ ┻━┻"
                    requests.post(post_url, data={"action": flip})
                    return jsonify({"winner": young_god})
                else:
                    seen.remove(data["position"])
                    my_move = choice(list(seen))
                    requests.post(post_url, data={"action": "putSymbol", "position": my_move})
                    seen.remove(my_move)
                    logging.info(f'Response: Remaining spots {seen}')
                    continue
            else:
                flip = "(╯°□°)╯︵ ┻━┻"
                requests.post(post_url, json={"action": flip})
                return jsonify({"winner": young_god})
        if 'winner' in data:
            return jsonify({"winner": data['winner']})


def with_requests(url):
    """Get a streaming response for the given event feed using requests."""
    return requests.get(url, stream=True)