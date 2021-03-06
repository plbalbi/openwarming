import requests, cachetools
from .github_service import APIError
from .exceptions import *

# t % curl -v 'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key=d865b95a583447a593b210600182308&q=Argentina&format=json&date=2018-04-11'|jq "."
WEATHER_API_KEY = "d865b95a583447a593b210600182308"

"""
@ aDate: Date object
@ aLocation: Locations as string
"""

# 365 element =~ roughly a year worth of dates data
cache = cachetools.LRUCache(365)

@cachetools.cached(cache)
def getDateAverageTemperature(aDate, aLocation):
    # Add date format
    formattedDate = "%d-%02d-%02d" % (aDate.year, aDate.month, aDate.day)
    # URLEncode location

    requestParams = {
        "key":WEATHER_API_KEY,
        "q":aLocation,
        "format":"json",
        "date":formattedDate
    }

    response = requests.get("http://api.worldweatheronline.com/premium/v1/past-weather.ashx", params = requestParams)

    if response.status_code != 200:
        # TODO: Add more error description in API Error class
        raise APIError(response)

    # .data.weather[0].maxtempC
    # .data.weather[0].mintempC
    weatherData = response.json()["data"]["weather"][0]

    maxTemp = float(weatherData["maxtempC"])
    minTemp = float(weatherData["mintempC"])

    return (maxTemp + minTemp) / 2