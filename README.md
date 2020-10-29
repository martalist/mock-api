# Mock API

--- 

## Australian vessel AIS data 

This is a mock API service that may be run locally to emulate a real-time service, such as [marinetraffic.com](https://www.marinetraffic.com/en/ais-api-services/documentation/api-service:ps05).

The data is from [AMSA](https://www.operations.amsa.gov.au/Spatial/DataServices/DigitalData), and covers all Australian waters for 2018. 

## Usage

1. First, ensure all requirements are installed (see `requirements.txt`)

2. Run `python3 http_server.py -s 01-01-2018 -p 1`. The arguments are 
  - `-s | start-date`: the start date. Any valid day in the year 2018 should be fine. The time will initialize to 12:00am UTC (8am WA time). If no `-s` argument is provided, the server will start two years ago from the current time.
  - `-p | --playback-speed`: the rate at which server time advances. If not specified it will default to `1.0`. Specifying `2.0` or `2` will cause time to advance at double the normal rate. `-p 8` results in 8x speed.

3. To fetch data, visit [localhost:5000](http://localhost:5000). Two GET parameters may be passed used:
  - `timestamp` specifies how far back in time to fetch data (from now). For example, `timestamp=10` requests the last 10 minutes of vessel data (relative to the server date/time specified in step #2). The default value is 10 (if the parameter is omitted from the url).
  - `craftid` specifies a single vessel ID, as a signed float. For example [localhost:5000/?timespan=1440&craftid=9415595744.0](http://localhost:5000/?timespan=1440&craftid=9415595744.0) will request 24 hours of data for the vessel with ID 9415595744.0. Omitting this parameter will fetch data for all vessels.
