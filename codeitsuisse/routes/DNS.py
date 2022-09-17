import sqlite3
import logging
import json
from flask import request, jsonify
from codeitsuisse import app
logger = logging.getLogger(__name__)
from codeitsuisse import app

conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute('''CREATE TABLE if not exists lookuptable (addr text not null, ip text not null)''')
class ListNode:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.hashmap = {}
        self.head = ListNode()
        self.tail = ListNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def move_node_to_tail(self, key):
            node = self.hashmap[key]
            node.prev.next = node.next
            node.next.prev = node.prev
            node.prev = self.tail.prev
            node.next = self.tail
            self.tail.prev.next = node
            self.tail.prev = node

    def get(self, key: int) -> int:
        if key in self.hashmap:
            self.move_node_to_tail(key)
        res = self.hashmap.get(key, -1)
        if res == -1:
            return res
        else:
            return res.value

    def put(self, key: int, value: int) -> None:
        if key in self.hashmap:
            self.hashmap[key].value = value
            self.move_node_to_tail(key)
        else:
            if len(self.hashmap) == self.capacity:
                self.hashmap.pop(self.head.next.key)
                self.head.next = self.head.next.next
                self.head.next.prev = self.head
            new = ListNode(key, value)
            self.hashmap[key] = new
            new.prev = self.tail.prev
            new.next = self.tail
            self.tail.prev.next = new
            self.tail.prev = new
input = {
  "lookupTable": {
    'google.com': '1.2.3.4',
    'amazon.com': '2.3.4.5',
    'yahoo.com': '3.4.5.6',
    'bing.com': '4.5.6.7',
    'facebook.com': '5.6.7.8',
    'instagram.com': '6.7.8.9'
  }
}
@app.route('/instantiateDNSLookup', methods=['POST'])
def part1():
    raw = request.get_json()
    logging.info("data sent is {}".format(raw))
    input = raw["lookupTable"]
    lookupTable = input
    for key, values in lookupTable.items():
        c.execute("INSERT INTO lookuptable (addr,ip) \
      VALUES (?,?)",(key, values))
        conn.commit()
    conn.close()
    return jsonify({
            "success": True
        })

@app.route('/simulateQuery', methods=['POST'])
def part2( ):
    raw = request.get_json()
    logging.info("data sent is {}".format(raw))
    size = raw["cacheSize"]
    log = raw["log"]
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    size = size
    log = log
    cache = LRUCache(size)
    json1 = []
    for i in log:
        if cache.get(i) == -1:
            cursor = c.execute("SELECT ip from lookuptable where addr = '" + i + "'")
            t = cursor.fetchall()
            if len(t) == 0:
                status = 'invalid'
                json1.append({"status": status, "ipAddress": 'Null'})
            for j in t:
                ip = j[0]
                status = 'cache miss'
                cache.put(i,ip)
                json1.append({"status": status, "ipAddress": ip})
                break
        else:
            status = 'cache hit'
            ip = cache.get(i)
            json1.append({"status": status, "ipAddress": ip})

    conn.close()
    logging.info("My crypto result :{}".format(json1))
    return json.dumps(json1)


