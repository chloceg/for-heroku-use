import logging
import json
import math

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/stig/warmup', methods=['POST'])
def swiss_stig_warmup():
    raw = request.get_json()
    logging.info("data sent {}".format(raw))
    result = []
    for i in raw:
        result.append(stig(i['questions'],i['maxRating']))
    
    logging.info("my result is {}".format(result))
    return jsonify(result)

def stig(questions,maxRating):
    questions = sorted(questions, key=lambda d: d['lower']) 
    count = 0
    for i in range(1,maxRating+1):
        pg = list(range(1,maxRating+1))
        for q in questions:
            if (i >= q["lower"] and i <= q["upper"]):
                pg = [x for x in pg if x >= q["lower"] and x <= q["upper"]]
            else:
                pg = [x for x in pg if x < q["lower"] or x > q["upper"]]
        if (i == min(pg)):
            count += 1
    d = math.gcd(count, maxRating)
    return {"p": count // d, "q": maxRating // d}


# def swiss_stig():
#     out = []
#     raw = request.get_json()
#     logging.info("data sent is {}".format(raw))
#     questions = raw[0]["questions"]
#     maxrating = raw[0]["maxRating"]
#     for i in range(len(questions)):
#         lower = questions[i]["lower"]
#         upper = questions[i]["upper"]
#         p = upper - lower + 1
#         q = maxrating
#         p //= math.gcd(maxrating, upper-lower+1)
#         q //= math.gcd(maxrating, upper-lower+1)
#         d = {}
#         d["p"], d["q"] = p, q
#         out.append(d)
#     logging.info("my result dict s {}".format(out))
#     return json.dumps(out)
