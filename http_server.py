#/usr/bin/python

import sys, getopt
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
import dataset

# To make a request from the API, visit the url below, where timespan is the
# number of minutes worth of data to fetch
# http://localhost:5000/?timespan=10

# Manages the server time/state
# Since this is historic data, the server's time must be in the past
# The default is 2 years ago, and can be changed using the -s or --start-date 
# command line argument.
ServerTime = { 'delta': timedelta(days=730), 'start': datetime.now() - timedelta(days=730) }

# Connect to the database once for the lifetime of the server
db = dataset.connect('sqlite:///maritimeData2018.sqlite')
app = Flask(__name__)


# helper function for adding '0' padding to a one digit number, as a string
# i.e. '2' --> '02'
def pad(string):
    if type(string) == int:
        string = str(string)
    if len(string) == 1:
        return '0' + string
    return string

# returns a SQLite compatible string representation of a datetime object
def date_str(dt):
    return f'{dt.year}-{pad(dt.month)}-{pad(dt.day)} {pad(dt.hour)}:{pad(dt.minute)}:{pad(dt.second)}'


@app.route('/', methods=['GET'])
def server():
    # process timespan parameter
    timespan = int(request.args.get('timespan', '10'))
    upper_bound = datetime.now() - ServerTime['delta']
    lower_bound = upper_bound - timedelta(minutes=timespan)

    # process craftid parameter
    craft_id = float(request.args.get('craftid')) if request.args.get('craftid') else None
    vessel_filter = "" if craft_id == None else f' AND craft_id = {craft_id}'

    # query the database
    query = 'SELECT * FROM PointData ' \
            f'WHERE datetime(timestamp) >= datetime(\'{date_str(lower_bound)}\') ' \
            f'AND datetime(timestamp) <= datetime(\'{date_str(upper_bound)}\'){vessel_filter};'
    results = db.query(query)

    # filter out the sqlite id - we don't need that
    result_list = [ { key: value for key, value in result.items() if key != 'id'} for result in results]

    # return as json
    return jsonify(dict(timespan=timespan, request_time=upper_bound.isoformat(), results=result_list, result_length=len(result_list)))


# helper method to print program usage
def print_usage(exit_code):
    print("usage: http_server.py [(-s | --start-date) DD-MM-YYYY]")
    sys.exit(exit_code)


# main function; starts the mock API
def main(argv):
    # parse command line arguments
    try:
        opts, args = getopt.getopt(argv, "hs:", ["--start-date="])
    except getopt.GetoptError:
        print_usage(2)
    for opt, value in opts:
        if opt == "-h":
            print_usage(0)
        elif opt in ("-s", "--start-date"):
            day, month, year = value.split('-')
            ServerTime['start'] = datetime(int(year), int(month), int(day))
            ServerTime['delta'] = datetime.now() - ServerTime['start']
    server_time = datetime.now() - ServerTime['delta']
    print(f'System date and time is {server_time}')

    # run the server
    app.run(host='localhost', port=5000)


if __name__ == '__main__':
    main(sys.argv[1:])
