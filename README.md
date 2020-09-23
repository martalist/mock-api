# Mock API

--- 

## Australian vessel AIS data 

This is a mock API service that may be run locally to emulate a real-time service, such as [marinetraffic.com](https://www.marinetraffic.com/en/ais-api-services/documentation/api-service:ps05).

The data is from [AMSA](https://www.operations.amsa.gov.au/Spatial/DataServices/DigitalData), and covers all Australian waters for 2018. 

## Usage

1. First, ensure all requirements are installed (see `requirements.txt`)

2. Run `python http_server.py -s 01-01-2018`. The argument is the start date. Any valid day in the year 2018 should be find.

3. To fetch data, visit [localhost:5000?timestamp=10](http://localhost:5000?timestamp=10). The `timestamp` argument specifies how far back in time to fetch data. Here `timestamp=10` requests the last 10 minutes of vessel data (relative to the server date/time specified in step #2).

