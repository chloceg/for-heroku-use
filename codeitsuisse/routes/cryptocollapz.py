import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/cryptocollapz', methods=['POST'])
def max_num():
    res = 0
    output = []
    d = {}
    raw = request.get_json()
    logging.info("data sent is {}".format(raw))
    nums = raw
    for entry in nums: # entry = [6,7,8,9,10]
        temp = []
        for item in entry:
            if item == 1 or item == 2:
                temp.append(4)
                continue
            x = item
            res = x
            while x != 1:
                if x in d:
                    break
                if x&1 == 1:
                    x = 3 * x + 1
                    res = max(res, x)
                else:
                    x = x // 2
                if x == 1:
                    d[item] = res
            temp.append(res)
        output.append(temp)
    r = output
    logging.info("My crypto result :{}".format(r))
    return json.dumps(r)
    # return output