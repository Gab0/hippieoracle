#!/bin/python

import requests
import json
import shutil
import os
from random import randrange, uniform, choice
import random
from time import time
from geopy import distance

import math


def get_map_image(coords):
    URL = 'https://maps.googleapis.com/maps/api/staticmap?center=%f,%f&zoom=12&size=1000x1000'
    return URL % (coords[0], coords[1])


def downloadMapImage(mapImageUrl, targetPath):
    a = requests.get(mapImageUrl, stream=True)
    with open(targetPath, 'wb') as f:
        shutil.copyfileobj(a.raw, f)


def calculateRealDistance(originCoordinates, targetCoordinates):
    return distance.distance(originCoordinates, targetCoordinates).km

def getCoordinates(originLatitude, originLongitude, minRadiusKM, maxRadiusKM):

    def calculateRadius(origin, minRadiusKM, maxRadiusKM):
        D = 0
        w = 0
        while D < maxRadiusKM:
            D = distance.distance(origin, (origin[0], origin[1] + w)).km
            w += 0.01
        m = w

        while D > minRadiusKM:
            D = distance.distance(origin, (origin[0], origin[1] + m)).km
            m -= 0.01
        return m, w

    def genRandomComponent(minradius, maxradius):
        a = uniform(minradius, maxradius)
        if random.random() < 0.5:
            a = -a
        return a

    def genDoubleRandomComponent(minRadius, maxRadius):
        return [genRandomComponent(minRadius, maxRadius)
                for r in range(2)]

    origin = (originLatitude, originLongitude)
    minRadius, maxRadius = calculateRadius(origin, minRadiusKM, maxRadiusKM)

    deltas = genDoubleRandomComponent(minRadius, maxRadius)

    radiusDistance = -1
    while radiusDistance > maxRadius or radiusDistance < minRadius:
        deltas = genDoubleRandomComponent(minRadius, maxRadius)
        radiusDistance = math.sqrt(deltas[0] ** 2 + deltas[1] ** 2)

    lat = originLatitude + deltas[0]
    lng = originLongitude + deltas[1]

    return lat, lng


def retrieve_locality(originLatitude, originLongitude, minradius, maxradius):

    def recursiveCall():
        return retrieve_locality(originLatitude, originLongitude, minradius, maxradius)
    lat, lng = getCoordinates(originLatitude, originLongitude,
                              minradius, maxradius)
    URL = "http://maps.googleapis.com/maps/api/geocode/json"

    Parameters = {'latlng': "%f,%f" % (lat, lng),
                  'sensor': 'false'}

    Request = requests.get(URL, params=Parameters)

    jsondata = json.loads(Request.text)

    Result = []
    print(json.dumps(jsondata, indent=4))
    if len(jsondata["results"]) == 0:
        return retrieve_locality(originLatitude,
                                 originLongitude,
                                 minradius,
                                 maxradius)

    result = jsondata["results"][0]

    ac = result["address_components"]
    print(ac)
    if len(ac) < 1:
        return recursiveCall()

    for component in ac:
        #if 'administrative_area_level_2' in component["types"]:
            #print('>>> %s' % component['short_name'])
            #Result.append(component['short_name'])
        ALLOWED = ['administrative_area_level_1', 'locality']
        for A in ALLOWED:
            if A in component['types']:
                Result.append(component['short_name'])

    if not len(Result) > 1:
        return recursiveCall()
    Result.append([lat, lng])

    middlelat = (originLatitude - lat)/2
    middlelat = middlelat + lat
    middlelng = (originLongitude - lng)/2
    middlelng = middlelng + lng

    print("Coord Origin: %f,%f   Middle: %f,%f   Destination: %f,%f" %
          (
              originLatitude,
              originLongitude,
              middlelat,
              middlelng,
              lat,
              lng
          )
    )

    Result.append([middlelat, middlelng])

    return Result


if __name__ == '__main__':
    W = retrieve_locality(-21.771, -41.35, 10, 200)
    print(get_map_image(W[3]))
