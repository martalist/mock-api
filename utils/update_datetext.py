#!/usr/bin/env python3

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
        if meridiem == "PM" and int(hours) < 12:
            hours = str(int(hours) + 12)
        if meridiem == "AM" and int(hours) == 12:
            hours = str(0)
        return f'{year}-{pad(month)}-{pad(day)} {pad(hours)}:{pad(minutes)}:{pad(seconds)}'
    return f'{year}-{pad(month)}-{pad(day)}'


db = dataset.connect('sqlite:///to_convert.sqlite')

to_update = []
for row in db['PointData'].all():
    if int(row['id']) > 10:
        result = format_date(row['timestamp'])
        to_update.append(dict(id=row['id'], timestamp=result))

for row in to_update:
    query = f"UPDATE PointData SET timestamp = '{row['timestamp']}' WHERE id = {row['id']};"
    #  print(query)
    db.query(query)
