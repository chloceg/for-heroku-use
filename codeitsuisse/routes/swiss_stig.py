import logging
import json
import math

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/stig/warmup', methods=['POST'])
def swiss_stig():
    raw = request.get_json()
    logging.info("data sent is {}".format(raw))
    questions = raw["questions"]
    maxrating = raw["maxRating"]
    lower = questions[0]["lower"]
    upper = questions[0]["upper"]
    p = upper - lower + 1
    q = maxrating
    p //= math.gcd(maxrating, upper-lower+1)
    q //= math.gcd(maxrating, upper-lower+1)
    d = {}
    d["p"], d["q"] = p, q
    logging.info("my result dict s {}".format(d))
    return json.dumps(d)