import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/cryptocollapz', methods=['POST'])
def max_num():
    res = 0
    output = []
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
                if x % 2 == 1:
                    x = 3 * x + 1
                elif x % 2 == 0:
                    x = int(x/2)
                res = max(res, x)
                # print(res)
            temp.append(res)
        output.append(temp)
    r = output
    logging.info("My crypto result :{}".format(r))
    return json.dumps(r)
    # return output