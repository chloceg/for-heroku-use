import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/tic-tac-toe', methods=['POST'])
def getid():
    data = request.get_json()
    logging.info('data sent for getid {}'.format(data))
    battleId = data.get('battleId')
    logging.info('battleId :{}'.format(battleId))
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
