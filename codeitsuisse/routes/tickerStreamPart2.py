import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/tickerStreamPart2', methods=['POST'])
def evaluate():
# def to_cumulative_delayed(stream: list, quantity_block: int):
    raw = request.get_json()
    logging.info("data sent is {}".format(raw))
    stream = raw.get("stream")
    quantity_block = raw.get("quantityBlock")
    cu_quan = 0
    cu_noti = 0
    d = []
    stream.sort(key = lambda x: x.split(',')[0])
    ticker = {}
    for i in stream:
        row = i.split(',')
        time = row[0]
        ticker[row[1]] = 1
        quant = int(row[2])
        price = float(row[3])
        d.append(row)
    dd = [[] for _ in ticker]
    cnt = 0
    for k in ticker:
        for i in d:
            if i[1] == k:
                dd[cnt].append([i[0], k, i[2], i[3]])
        cnt += 1
    res = []
    for d in dd:
        for i in range(len(d)):
            if cu_quan + int(d[i][2]) == quantity_block:
                cu_noti += round(int(d[i][2])*float(d[i][3]), 1)
                cu_quan += int(d[i][2])
                res.append(','.join([d[i][0], d[i][1], str(quantity_block), str(cu_noti)]))
                cu_quan, cu_noti = 0, 0
            elif cu_quan + int(d[i][2]) > quantity_block:
                cu_noti += int(quantity_block - cu_quan) * round(float(d[i][3]), 1)
                cu_quan += quantity_block - int(d[i][2])
                res.append(','.join([d[i][0], d[i][1], str(quantity_block), str(cu_noti)]))
                cu_quan, cu_noti = 0, 0
            else:
                cu_noti += round(int(d[i][2])*float(d[i][3]), 1)
                cu_quan += int(d[i][2])
    res.sort(key = lambda x: x.split(',')[0])
    return json.dumps(res)