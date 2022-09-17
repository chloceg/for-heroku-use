import logging
import json
import math

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/stig/warmup', methods=['POST'])
def swiss_stig():
    out = []
    raw = request.get_json()
    logging.info("data sent is {}".format(raw))
    questions = raw[0]["questions"]
    maxrating = raw[0]["maxRating"]
    for i in range(len(questions)):
        lower = questions[i]["lower"]
        upper = questions[i]["upper"]
        p = upper - lower + 1
        q = maxrating
        p //= math.gcd(maxrating, upper-lower+1)
        q //= math.gcd(maxrating, upper-lower+1)
        d = {}
        d["p"], d["q"] = p, q
        out.append(d)
    logging.info("my result dict s {}".format(out))
    return json.dumps(out)