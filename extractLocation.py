import geopy
import pandas as pd
import json
import sys
from geopy.extra.rate_limiter import RateLimiter

data = pd.read_csv("responses.csv")
geolocator = geopy.geocoders.OpenMapQuest(
    api_key=sys.argv[1], timeout=1)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1, max_retries=3)
locationStrings = data.iloc[:, 3].tolist()
locations = {}
locationsNotFound = {}

for locationString in locationStrings:
    if not locationString in locations:
        print(locationString)
        location = geocode(
            locationString, addressdetails=True)
        if not location is None:
            locations[locationString] = location.raw
        else:
            locationsNotFound[locationString] = ""

with open('locationData_new.json', 'w') as outfile:
    json.dump(locations, outfile)
with open('locationsNotFound_new.json', 'w') as outfile:
    json.dump(locationsNotFound, outfile)
