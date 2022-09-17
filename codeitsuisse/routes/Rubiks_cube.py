import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

from codeitsuisse import app

@app.route('/rubiks', methods=['POST'])
def mian():
    raw = request.get_json()
    logging.info("data sent is {}".format(raw))
    ops = raw["ops"]
    state = raw["state"]
    res = []
    if ops == '':
        r = {"state":state}
        return json.dumps(r)
    elif len(ops) < 2:
        res.append(ops[0])
    else:
        ops = ops.split('i')
        for i, num in enumerate(ops):
            if len(num) == 1 and i < len(ops) - 1:
                res.append(num+'i')
            else:
                for j in num:
                    res.append(j)
                
    cube = [[] for _ in range(6)]
    seq = ['f', 'b', 'l', 'r', 'u', 'd']
    for idx, cul in enumerate(seq):
        cube[idx] = [j for item in state[cul] for j in item]

    def surface_rotate(l, times=1, direction=1):
        one_time = [(0, 2), (0, -1), (0, -3), (1, 3), (3, -2), (-2, -4)]
        two_times = [(0, -1), (1, -2), (2, -3), (3, -4)]

        if times == 1:
            index = one_time
        else:
            index = two_times

        if not direction:
            index.reverse()
        for i, j in index:
            l[i], l[j] = l[j], l[i]


    def rotate(cube, cmd):
        if cmd == "o":
            cube[2], cube[3] = cube[3], cube[2]
            cube[0], cube[1] = cube[1], cube[0]
            surface_rotate(cube[4], 2)
            surface_rotate(cube[5], 2)
        elif cmd == "yi":
            index = [(0, 3), (0, 1), (0, 2)]
            for i, j in index:
                cube[i], cube[j] = cube[j], cube[i]
            surface_rotate(cube[4], 1, 0)
            surface_rotate(cube[5], 1, 1)
        elif cmd == "y":
            index = [(0, 2), (0, 1), (0, 3)]
            for i, j in index:
                cube[i], cube[j] = cube[j], cube[i]
            surface_rotate(cube[4], 1, 1)
            surface_rotate(cube[5], 1, 0)

        elif cmd == "xi":
            index = [(0, 5), (0, 1), (0, 4)]
            for i, j in index:
                cube[i], cube[j] = cube[j], cube[i]
            surface_rotate(cube[1], 2)
            surface_rotate(cube[4], 2)
            surface_rotate(cube[2], 1, 1)
            surface_rotate(cube[3], 1, 0)

        elif cmd == "x":
            index = [(0, 4), (0, 1), (0, 5)]
            for i, j in index:
                cube[i], cube[j] = cube[j], cube[i]
            surface_rotate(cube[1], 2)
            surface_rotate(cube[5], 2)
            surface_rotate(cube[2], 1, 0)
            surface_rotate(cube[3], 1, 1)

    def whole_rotate(cube, cmd):
        if cmd == "o":
            cube[2], cube[3] = cube[3], cube[2]
            cube[0], cube[1] = cube[1], cube[0]
            surface_rotate(cube[4], 2)
            surface_rotate(cube[5], 2)
        elif cmd == "yi":
            index = [(0, 3), (0, 1), (0, 2)]
            for i, j in index:
                cube[i], cube[j] = cube[j], cube[i]
            surface_rotate(cube[4], 1, 0)
            surface_rotate(cube[5], 1, 1)

        elif cmd == "y":
            index = [(0, 2), (0, 1), (0, 3)]
            for i, j in index:
                cube[i], cube[j] = cube[j], cube[i]
            surface_rotate(cube[4], 1, 1)
            surface_rotate(cube[5], 1, 0)

        elif cmd == "xi":
            index = [(0, 5), (0, 1), (0, 4)]
            for i, j in index:
                cube[i], cube[j] = cube[j], cube[i]
            surface_rotate(cube[1], 2)
            surface_rotate(cube[4], 2)
            surface_rotate(cube[2], 1, 1)
            surface_rotate(cube[3], 1, 0)

        elif cmd == "x":
            index = [(0, 4), (0, 1), (0, 5)]
            for i, j in index:
                cube[i], cube[j] = cube[j], cube[i]
            surface_rotate(cube[1], 2)
            surface_rotate(cube[5], 2)
            surface_rotate(cube[2], 1, 0)
            surface_rotate(cube[3], 1, 1)

            
    def rotate_front_layer(cube, direction=1):
        face_index = [
            [(2, 4), [(2, 8), (5, 7), (8, 6)]],
            [(2, 3), [(2, 6), (5, 3), (8, 0)]],
            [(2, 5), [(2, 0), (5, 1), (8, 2)]]
            ]
        if not direction:
            face_index.reverse()
        surface_rotate(cube[0], 1, direction)
        for idx in face_index:
            f_1, f_2 = idx[0]
            for clr_1, clr_2 in idx[1]:
                cube[f_1][clr_1], cube[f_2][clr_2] = cube[f_2][clr_2], cube[f_1][clr_1]        

    def rules(cube, cmd):
        cmd_dict = {
            "L": ["yi", 1, "y"],
            "Li": ["yi", 0, "y"],
            "R": ["y", 1, "yi"],
            "Ri": ["y", 0, "yi"],
            "U": ["xi", 1, "x"],
            "Ui": ["xi", 0, "x"],
            "D": ["x", 1, "xi"],
            "Di": ["x", 0, "xi"],
            "F": ["", 1, ""],
            "Fi": ["", 0, ""],
            "B": ["o", 1, "o"],
            "Bi": ["o", 0, "o"]
        }
        func_list = [whole_rotate, rotate_front_layer, whole_rotate]
        cmd_list = cmd_dict[cmd]
        for i in range(3):
            func_list[i](cube, cmd_list[i])
    for f in res:
        rules(cube, f)
    for idx, j in enumerate(seq):
        state[j][0] = cube[idx][0:3]
        state[j][1] = cube[idx][3:6]
        state[j][2] = cube[idx][6:9]

    logging.info("My state result :{}".format(state))
    r = {state}
    return json.dumps(r)
