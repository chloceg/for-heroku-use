# import logging
# import json
# from flask import request, jsonify
# from codeitsuisse import app
# from codeitsuisse import app
#logger = logging.getLogger(__name__)
input = [
  "4, 3, 3",
  "4, 3, 3, 0, 0, 0, 1"
]
#@app.route('/social-distancing', methods=['POST'])
def simulation(input):
    for i in input:
        t = i.split(',')
        width = t[0]
        height = t[1]
        people = t[2]
        table = [ [0 for col in range(int(width))] for row in range(int(height))]
    return

simulation(input)