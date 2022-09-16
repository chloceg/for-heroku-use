import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/tickerStreamPart1', methods=['POST'])
def to_cumulative():
    # data = request.get_json()
    # logging.info("data sent for evaluation {}".format(data))
    # inputValue = data.get("input")
    # result = inputValue * inputValue
    # logging.info("My result :{}".format(result))
    # return json.dumps(result)
    d = {}
    raw = request.get_json()
    logging.info("data sent is {}".format(raw))
    stream = raw.get("stream")
    stream.sort(key = lambda x: x.split(',')[1])
    for i in stream:
        row = i.split(',')
        time = row[0]
        ticker = row[1]
        quant = int(row[2])
        price = float(row[3])
        if time not in d.keys():
            d[time] = [[ticker, quant, price]]
        else:
            d[time].append([ticker, quant, price])
    r = {}
    for i in d:
        length = len(d[i])
        for j in range(length):
            alpha = d[i][j]
            if alpha[0] not in r:
                r[alpha[0]] = [round(alpha[1], 1), round(alpha[2]*alpha[1], 1)]
            else:
                r[alpha[0]] = [round(r[alpha[0]][0]+alpha[1], 1), round(r[alpha[0]][1]+alpha[2]*alpha[1], 1)]
            out = ''
            out += i
        for k in r.keys():
            res = ','.join([k, str(r[k][0]), str(r[k][1])])
            out = out + ',' + res
        logging.info("My part1 result :{}".format([out]))
        return json.dumps([out])
        # return [out]
