import logging
import json
import pandas as pd
import numpy as np

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/tickerStreamPart1', methods=['POST'])
def to_cumulative():
    d = {}
    raw = request.get_json()
    logging.info("data sent is {}".format(raw))
    stream = raw.get("stream")
    df = pd.DataFrame(stream)
    df = df.iloc[:, 0].str.split(',', expand=True)
    df[2] = df[2].astype(np.int8)
    df[3] = df[3].astype(np.float32)
    df[4] = np.round(df[2] * df[3],decimals=1)
    df.sort_values([0,1], ascending=True, inplace=True)
    df[2] = df[2].astype(str)
    df[4] = df[4].astype(str)
    pre_time = df.iloc[0,:,][0]
    result = []
    tick = ''+pre_time
    for i in df.iterrows():
      if i[1][0] != pre_time:
          result.append(tick)
          pre_time = i[1][0]
          tick = ''+pre_time
      temp = ','.join([i[1][1], i[1][2], i[1][4]])
      tick = tick +','+temp
    result.append(tick)
    r = {"output": result}

#     stream.sort(key = lambda x: [x.split(',')[0], x.split(',')[1]])
#     for i in stream:
#         row = i.split(',')
#         time = row[0]
#         ticker = row[1]
#         quant = int(row[2])
#         price = float(row[3])
#         if time not in d.keys():
#             d[time] = [[ticker, quant, price]]
#         else:
#             d[time].append([ticker, quant, price])
#     r = {}
#     output = []
#     for i in d:
#         length = len(d[i])
#         for j in range(length):
#             alpha = d[i][j]
#             if alpha[0] not in r:
#                 r[alpha[0]] = [round(alpha[1], 1), round(alpha[2]*alpha[1], 1)]
#             else:
#                 r[alpha[0]] = [round(r[alpha[0]][0]+alpha[1], 1), round(r[alpha[0]][1]+alpha[2]*alpha[1], 1)]
#             out = ''
#             out += i
#         for k in r.keys():
#             res = ','.join([k, str(r[k][0]), str(r[k][1])])
#             entry = out + ',' + res
#             output.append(entry)
#     r = {"output": output}
    logging.info("My part1 result :{}".format(r))
    return json.dumps(r)
    # return [out]
