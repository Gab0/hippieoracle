#!/bin/python
import os
import requests
import json
import pandas as pd


def fetchOnline(query, apikey):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        "address": query,
        "key": apikey
    }
    a = requests.get(base_url, params=params)
    r = a.json()
    print("____")
    print(json.dumps(r, indent=2))

    if r["results"]:
        location = r["results"][0]["geometry"]["location"]
        location["Location"] = query
        return location

    else:
        return None


def fetch(query, filePath, apikey):
    a = loadLocations(filePath)
    print(a)
    recorded = list(a.Location)
    print(query)
    print(recorded)
    if a is not None and query in recorded:
        print(">>>>")
        W = a[a.Location == query].iloc[0]
        return W

    else:
        location = fetchOnline(query, apikey)
        if location is not None:
            a.append(location)
            a.to_csv(filePath)
            return location
        else:
            return None


def loadLocations(filePath):
    if os.path.isfile(filePath):
        locations = pd.read_csv(filePath)
        return locations
    else:
        return None


# unused
def writeLocations(locations):
    locations.to_csv(filePath)
    
