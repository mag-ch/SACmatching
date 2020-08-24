import geopy
import json
import sys
from geopy.extra.rate_limiter import RateLimiter

print(sys.argv)
geolocator = geopy.geocoders.OpenMapQuest(
    api_key=sys.argv[1], timeout=1)
locationString = 'Baltimore, MD, USA'
location = geolocator.geocode(
    locationString, addressdetails=True)
print(location.raw)
