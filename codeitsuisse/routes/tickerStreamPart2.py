# import logging
# import json
# import numpy as np
# from flask import request, jsonify

# from codeitsuisse import app

# logger = logging.getLogger(__name__)

# @app.route('/tickerStreamPart2', methods=['POST'])
# # def to_cumulative_delayed():
# # # def to_cumulative_delayed(stream: list, quantity_block: int):
# #     raw = request.get_json()
# #     logging.info("data sent is {}".format(raw))
# #     stream = raw.get("stream")
# #     quantity_block = raw.get("quantityBlock")
# #     cu_quan = 0
# #     cu_noti = 0
# #     d = []
# #     stream.sort(key = lambda x: x.split(',')[0])
# #     ticker = {}
# #     for i in stream:
# #         row = i.split(',')
# #         time = row[0]
# #         ticker[row[1]] = 1
# #         quant = int(row[2])
# #         price = float(row[3])
# #         d.append(row)
# #     dd = [[] for _ in ticker]
# #     cnt = 0
# #     for k in ticker:
# #         for i in d:
# #             if i[1] == k:
# #                 dd[cnt].append([i[0], k, i[2], i[3]])
# #         cnt += 1
# #     res = []
# #     for d in dd:
# #         for i in range(len(d)):
# #             if cu_quan + int(d[i][2]) == quantity_block:
# #                 cu_noti += round(int(d[i][2])*float(d[i][3]), 1)
# #                 cu_quan += int(d[i][2])
# #                 res.append(','.join([d[i][0], d[i][1], str(quantity_block), str(cu_noti)]))
# #                 cu_quan, cu_noti = 0, 0
# #             elif cu_quan + int(d[i][2]) > quantity_block:
# #                 cu_noti += int(quantity_block - cu_quan) * round(float(d[i][3]), 1)
# #                 cu_quan += quantity_block - int(d[i][2])
# #                 res.append(','.join([d[i][0], d[i][1], str(quantity_block), str(cu_noti)]))
# #                 cu_quan, cu_noti = 0, 0
# #             else:
# #                 cu_noti += round(int(d[i][2])*float(d[i][3]), 1)
# #                 cu_quan += int(d[i][2])
# #     res.sort(key = lambda x: x.split(',')[0])
# #     r = {"output": res}
# #     logging.info("My part2 result :{}".format(r))
# #     return json.dumps(r)


# def to_cumulative_delayed():
#     raw = request.get_json()
#     logging.info("data sent is {}".format(raw))
#     stream = raw.get("stream")
#     quantity_block = raw.get("quantityBlock")
#     temp = []
#     list = []
#     for i in stream:
#         if temp != []:
#             list.append(temp)
#         temp = []
#         for j in i.split(','):
#             temp.append(j)
#     list.append(temp)
#     list = np.array(list)
#     list = list[np.lexsort([list[:, 0], list[:, 1]]), :]
#     temp_block = int(0)
#     dict = {}
#     role = ''
#     output = []
#     for i in list:
#         if role != i[1]:
#             role = i[1]
#             temp_block = 0
#             dict = {}
#         if '' in i:
#             continue
#         if int(int(i[2]) + temp_block) <= quantity_block:
#             if dict.get(i[1]) != None:
#                 q, n = dict[i[1]].split(',')[0], dict[i[1]].split(',')[1]
#                 dict[i[1]] = str(int(i[2]) + int(q)) + ',' + str(
#                     round(int(i[2]) * float(i[3]) + float(n), 1))
#             else:
#                 dict[i[1]] = str(int(i[2])) + ',' + str(
#                     round(int(i[2]) * float(i[3]), 1))
#             temp_block = temp_block + int(i[2])
#             if temp_block == quantity_block:
#                 temp_block = 0
#                 output.append(i[0] + ',' + role + ',' +
#                               dict[role].split(',')[0] + ',' +
#                               dict[role].split(',')[1])
#                 dict = {}
#         else:
#             i[2] = int(i[2]) - 5 + temp_block
#             if dict.get(i[1]) != None:
#                 q, n = dict[i[1]].split(',')[0], dict[i[1]].split(',')[1]
#                 dict[i[1]] = str(quantity_block) + ',' + str(
#                     round(int(5 - temp_block) * float(i[3]) + float(n), 1))
#             else:
#                 dict[i[1]] = str(int(i[2])) + ',' + str(
#                     round(int(i[2]) * float(i[3]), 1))
#             output.append(i[0] + ',' + role + ',' + dict[role].split(',')[0] +
#                           ',' + dict[role].split(',')[1])
#             times = int(i[2]) // quantity_block
#             temp_block = int(i[2]) % quantity_block
#             dict[i[1]] = str(temp_block) + ',' + str(
#                 round(int(temp_block) * float(i[3]), 1))
#             if times >= 1:
#                 for j in range(0, times - 1):
#                     output.append(i[0] + ',' + role + ',' +
#                                   str(quantity_block) + ',' +
#                                   str(quantity_block * float(i[3])))
#     temp = []
#     t = []
#     for i in output:
#         if temp != []:
#             t.append(temp)
#         temp = []
#         for j in i.split(','):
#             temp.append(j)
#     output = []
#     t.append(temp)
#     t = np.array(t)
#     t = t[np.lexsort([t[:, 1], t[:, 0]]), :].tolist()
#     for i in t:
#         output.append(i[0] + ',' + i[1] + ',' + i[2] + ',' + i[3])
#     return output



import logging
import json
import pandas as pd
import numpy as np
from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/tickerStreamPart2', methods=['POST'])
def to_cumulative_delayed():
    raw = request.get_json()
    logging.info("data sent is {}".format(raw))
    stream = raw.get("stream")
    quantity_block = raw.get("quantityBlock")
    stream.sort(key = lambda x: x.split(',')[0])
    df = pd.DataFrame(stream)
    df = df.iloc[:, 0].str.split(',', expand=True)
    df[2] = df[2].astype(np.int8)
    df[3] = df[3].astype(np.float32)
    labels = df[1].unique()
    quantity_block = 5
    result = []
    for i in labels:
        temp = df[df[1] == i]
        cumu_quantity, cumu_national = 0, 0
        for j in temp.iterrows():
            if cumu_quantity + j[1][2] == quantity_block:
                cumu_national +=  round((j[1][2] * j[1][3]), 1)
                cumu_quantity += j[1][2]
                result.append(','.join([j[1][0], j[1][1], str(cumu_quantity), str(cumu_national)]))
                cumu_quantity, cumu_national = 0, 0
    
            elif cumu_quantity + j[1][2] < quantity_block:
                cumu_national +=  round((j[1][2] * j[1][3]), 1)
                cumu_quantity += j[1][2]
            elif cumu_quantity + j[1][2] > quantity_block:
                cumu_national += round((quantity_block - cumu_quantity) * j[1][3],1)
                cumu_quantity = quantity_block
                result.append(','.join([j[1][0], j[1][1], str(cumu_quantity), str(cumu_national)]))
                cumu_quantity, cumu_national = 0, 0
    result.sort(key=lambda x: x.split(',')[0])
    r = {"output": result}
    logging.info("My part2 result :{}".format(r))
    return json.dumps(r)


    # return result
# def to_cumulative_delayed():
# # def to_cumulative_delayed(stream: list, quantity_block: int):
#     raw = request.get_json()
#     logging.info("data sent is {}".format(raw))
#     stream = raw.get("stream")
#     quantity_block = raw.get("quantityBlock")
#     cu_quan = 0
#     cu_noti = 0
#     d = []
#     stream.sort(key = lambda x: x.split(',')[0])
#     ticker = {}
#     for i in stream:
#         row = i.split(',')
#         time = row[0]
#         ticker[row[1]] = 1
#         quant = int(row[2])
#         price = float(row[3])
#         d.append(row)
#     dd = [[] for _ in ticker]
#     cnt = 0
#     for k in ticker:
#         for i in d:
#             if i[1] == k:
#                 dd[cnt].append([i[0], k, i[2], i[3]])
#         cnt += 1
#     res = []
#     for d in dd:
#         for i in range(len(d)):
#             if cu_quan + int(d[i][2]) == quantity_block:
#                 cu_noti += round(int(d[i][2])*float(d[i][3]), 1)
#                 cu_quan += int(d[i][2])
#                 res.append(','.join([d[i][0], d[i][1], str(quantity_block), str(cu_noti)]))
#                 cu_quan, cu_noti = 0, 0
#             elif cu_quan + int(d[i][2]) > quantity_block:
#                 cu_noti += int(quantity_block - cu_quan) * round(float(d[i][3]), 1)
#                 cu_quan += quantity_block - int(d[i][2])
#                 res.append(','.join([d[i][0], d[i][1], str(quantity_block), str(cu_noti)]))
#                 cu_quan, cu_noti = 0, 0
#             else:
#                 cu_noti += round(int(d[i][2])*float(d[i][3]), 1)
#                 cu_quan += int(d[i][2])
#     res.sort(key = lambda x: x.split(',')[0])
#     r = {"output": res}
#     logging.info("My part2 result :{}".format(r))
#     return json.dumps(r)