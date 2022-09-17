import datetime
# input = [2021, 1, 2, 60, 38, 40, 39, 42, 41, 91]
import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/calendarDays', methods=['POST'])
def main():
    raw = request.get_json()
    logging.info("data sent is {}".format(raw))
    input = raw["numbers"]

    def calendar_cal(input):
        output = ''
        w= {'1':'       ', '2':'       ', '3':'       ', '4':'       ', '5':'       ', '6':'       ',
            '7':'       ', '8':'       ', '9':'       ', '10':'       ', '11':'       ', '12':'       '}
        t = 0
        isLeap = lambda y: y % 400 == 0 or (y % 4 == 0 and y % 100 != 0)
        for i in input:
            if t == 0:
                year = i
                stamp = datetime.date(year,1,1)
                t += 1
            elif (i<366 and i > 0) or (i<=366 and i > 0 and isLeap(year)):
                m = month(year,i)
                if w[m] == 'alldays':
                    continue
                else:
                    temp_w = week(stamp.weekday(),i%7)
                    if len(w[m]) == 7 and w[m][(i + stamp.weekday() - 1)%7] == temp_w:
                        continue
                    elif w[m] == 'weekday':
                        if ((i + stamp.weekday() - 1)%7) < 5:
                            continue
                        else:
                            w[m] = 'mtwtf  '
                            #w[m][(i - 3) % 7] = week(i % 7)
                            w[m] = change_str(w[m], (i + stamp.weekday() - 1) % 7, week(stamp.weekday(),i % 7))
                            continue
                    elif w[m] == 'weekend':
                        if ((i + stamp.weekday() - 1) % 7) >= 5:
                            continue
                        else:
                            w[m] = '     ss'
                            #w[m][(i - 3) % 7] = week(i%7)
                            w[m] = change_str(w[m], (i + stamp.weekday() - 1) % 7, week(stamp.weekday(),i % 7))
                            continue
                    elif w[m] != 'weekday' and w[m] != 'weekend':
                        #w[m][(i - 3) % 7] = week(i%7)
                        w[m] = change_str(w[m],(i + stamp.weekday() - 1) % 7, week(stamp.weekday(),i%7))

                    if w[m] == 'mtwtf  ':
                        w[m] = 'weekday'
                    elif w[m] == '     ss':
                        w[m] = 'weekend'
                    elif w[m] == 'mtwtfss':
                        w[m] = 'alldays'
        for i in range (0,12):
            output += w[str(i+1)] + ','
        return output

    def month(year,d):
        isLeap = lambda y: y % 400 == 0 or (y % 4 == 0 and y % 100 != 0)
        if not isLeap(year):
            if d > 0 and d <= 31:
                return '1'
            elif d > 31 and d <= 59:
                return '2'
            elif d > 59 and d <= 90:
                return '3'
            elif d > 90 and d <= 120:
                return '4'
            elif d > 120 and d <= 151:
                return '5'
            elif d > 151 and d <= 181:
                return '6'
            elif d > 181 and d <= 212:
                return '7'
            elif d > 212 and d <= 243:
                return '8'
            elif d > 243 and d <= 273:
                return '9'
            elif d > 273 and d <= 304:
                return '10'
            elif d > 304 and d <= 334:
                return '11'
            elif d > 334 and d <= 365:
                return '12'
        else:
            if d > 0 and d <= 31:
                return '1'
            elif d > 31 and d <= 60:
                return '2'
            elif d > 60 and d <= 91:
                return '3'
            elif d > 91 and d <= 121:
                return '4'
            elif d > 121 and d <= 152:
                return '5'
            elif d > 152 and d <= 182:
                return '6'
            elif d > 182 and d <= 213:
                return '7'
            elif d > 213 and d <= 244:
                return '8'
            elif d > 244 and d <= 274:
                return '9'
            elif d > 274 and d <= 305:
                return '10'
            elif d > 305 and d <= 335:
                return '11'
            elif d > 335 and d <= 366:
                return '12'


    def week(stamp, d):
        d += (stamp-1)
        d = d % 7
        if d == 0:
            return 'm'
        elif d == 1:
            return 't'
        elif d == 2:
            return 'w'
        elif d == 3:
            return 't'
        elif d == 4:
            return  'f'
        elif d == 5:
            return  's'
        elif d == 6:
            return 's'

    def change_str(s, p, v):
        newlist = []
        newstr = ''
        for i in range(0, len(s)):
            if i <= len(s) - 1:
                if i != p:
                    newlist.append(s[i])
                else:
                    newlist.append(v)
        for n in newlist:
            newstr += n
        return newstr

    def inverse_calendar(string,year):
        t = 0
        list = []
        w = {'0':'','1':'','2':'','3':'','4':'','5':'','6':'','7':'','8':'','9':'','10':'','11':''}
        for i in string.split(','):
            if t == 12:
                break
            stamp = datetime.date(year, t+1, 1).weekday()
            if i == '       ':
                continue
            if i == 'alldays':
                i = 'mtwtfss'
            elif i == 'weekday':
                i = 'mtwtf  '
            elif i == 'weekend':
                i = '     ss'
            s = 0
            for j in i:
                if j != ' ':
                    for x in range (0,7):
                        if (x + stamp) % 7 == (s % 7):
                            list.append(dayOfYear(year, int(t+1), x + 1))
                s += 1
            t += 1
        return sorted(list)

    def dayOfYear(year, month, day):
        isLeap = lambda y: y % 400 == 0 or (y % 4 == 0 and y % 100 != 0)
        y, m, d = year, month, day
        month = [31, 29 if isLeap(y) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        return sum(month[:m - 1]) + d

    part1 = calendar_cal(input)
    part2 = [2001] + inverse_calendar(part1, 2001)
    r = {
        "part1": part1,
        "part2": part2
    }
    logging.info("My crypto result :{}".format(r))
    return json.dumps(r)
