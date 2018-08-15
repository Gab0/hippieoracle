#!/bin/python

import requests
import json
import shutil
import os
from random import randrange, uniform, choice
import random
from time import time

googleApiKey = 'AIzaSyAN8DCnslHInk8dHFFQIPPI9-W-eP4sly8'
W = "7OxgwSvRximk1EpjHCnVuCKSJGM="


def trigger(self, message):
    if '@hippie' in message:
        Result = retrieve_locality(-21.771, -41.35, 0.5)
        if ' moderno' in output:
            self.sendimage(sender, get_map_image(Result[3]))
        Flavor = ['vagabundear', 'passear', 'vender seus artesanatos',
                      'manguear']
        F = choice(Flavor)
        return "Voce devia ir %s em %s/%s..." % (F, Result[0], Result[1])
    else:
        return None


def get_map_image(coords):
    URL = 'https://maps.googleapis.com/maps/api/staticmap?center=%f,%f&zoom=12&size=1000x1000'
    return URL % (coords[0], coords[1])


def downloadMapImage(mapImageUrl, targetPath):
    a = requests.get(mapImageUrl, stream=True)
    with open(targetPath, 'wb') as f:
        shutil.copyfileobj(a.raw, f)


def getCoordinates(originLatitude, originLongitude, minradius, maxradius):

    def genRandomComponent(minradius, maxradius):
        a = uniform(minradius, maxradius)
        if random.random() < 0.5:
            a = -a
        return a
    lat = originLatitude + genRandomComponent(minradius, maxradius)
    lng = originLongitude + genRandomComponent(minradius, maxradius)
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
    W = retrieve_locality(-21.771, -41.35, 0.2, 0.5)
    print(get_map_image(W[3]))
