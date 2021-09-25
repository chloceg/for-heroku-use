import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/tic-tac-toe/'+battleId, methods=['POST'])
def chess():
    data = request.get_json()
    logging.info('data sent for chess {}'.format(data))
    action = data.get('action')
    position = data.get('position')
    return json.dumps(action, position)

