#!/usr/bin/python

import dataset

def pad(string):
    if len(string) == 1:
        return '0' + string
    return string

def format_date(dtext):
    try:
        # some records don't have a time
        date, time, meridiem = dtext.split(' ')
    except ValueError:
        date = dtext
        time = ""

    day, month, year = date.split('/')
    if time != "":
        hours, minutes, seconds = time.split(':')
        if (meridiem == "PM"):
            hours = str(int(hours) + 12)
        return f'{year}-{pad(month)}-{pad(day)} {pad(hours)}:{pad(minutes)}:{pad(seconds)}'
    return f'{year}-{pad(month)}-{pad(day)}'


db = dataset.connect('sqlite:///to_convert.sqlite')

table = db['PointData']
for row in table.all():
    result = format_date(row['timestamp'])
    #  print(row)
    # updated = row.copy()
    # updated['timestamp'] = result
    row_update = dict(id=row['id'], timestamp=result)
    table.update(row_update, ['id'])
    #  print(row)
    #  print(result)
