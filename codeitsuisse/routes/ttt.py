import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/tic-tac-toe', methods=['POST'])
'''
def evaluate():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("input")
    result = inputValue * inputValue
    logging.info("My result :{}".format(result))
    return json.dumps(result)
'''

def getid():
    data = request.get_json()
    logging.info("data sent for getid {}".format(data))
    battleId = data.get("battleId")
    logging.info("battleId :{}".format(battleId))
    return json.dumps(battleId)

