import logging
import json
import numpy as np

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def crypto_collapz_stream(data):
    res = []
    for input in data:
        res.append(crypto_collapz_raw(input))
    return res

def crypto_collapz_raw(input):
    res = []
    map = {
        1: 4
        }
    for item in input:
        res.append(lar(item, map))
    return res

def lar(num, map):
    if num in map:
        return map[num]
    map[num] = num
    cur = num    
    while True:
        if int(cur)&1:
            cur = 3*cur+1
            map[num] = max(map[num], cur)   # local 
        else:
            cur = cur//2
        if cur in map:
            map[num] = max(map[num], map[cur])  # local  > current
            break
        if cur == num:
            break
    return int(map[num])


@app.route('/cryptocollapz', methods=['POST'])
def crypto_collapz():
    data = request.get_json()
    logging.info("data sent is {}".format(data))
    r = crypto_collapz_stream(data)
    logging.info("my result is {}".format(r))
    return jsonify(r)

# def max_num():
# 	stream = request.get_json()
# 	arr = np.asarray(stream)
	
# 	for price in np.nditer(arr, op_flags=['readwrite'], flags=["refs_ok"]):
# 		if price == 1 or price == 2:
# 			price = 4
# 		else:
# 			temp = price
# 			while price != 1:
# 				if price > temp:
# 					temp = price
# 				price = collatz(price)
# 			price = temp
# 	return json.dumps(arr.tolist())

# def max_num():
#     res = 0
#     output = []
#     d = {}
#     raw = request.get_json()
#     logging.info("data sent is {}".format(raw))
#     nums = raw
#     for entry in nums: # entry = [6,7,8,9,10]
#         temp = []
#         for item in entry:
#             if item == 1 or item == 2:
#                 temp.append(4)
#                 continue
#             x = item
#             res = x
#             while x != 1:
#                 if x in d:
#                     break
#                 if x&1 == 1:
#                     x = 3 * x + 1
#                     res = max(res, x)
#                 else:
#                     x = x // 2
#                 if x == 1:
#                     d[item] = res
#             temp.append(res)
#         output.append(temp)
#     r = output
#     logging.info("My crypto result :{}".format(r))
#     return json.dumps(r)
#     # return output