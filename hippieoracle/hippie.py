#!/bin/python

import requests
import json
from random import randrange, uniform, choice
from time import time

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
    URL = 'https://maps.googleapis.com/maps/api/staticmap?center=%f,%f&zoom=12&size=640x480&key=AIzaSyAN8DCnslHInk8dHFFQIPPI9-W-eP4sly8'
    return URL % (coords[0], coords[1])
def retrieve_locality(originLatitude, originLongitude, radius):

    lat = originLatitude + uniform(-radius, radius)
    lng = originLongitude + uniform(-radius, radius)

    URL = "http://maps.googleapis.com/maps/api/geocode/json"

    Parameters = {'latlng': "%f,%f" % (lat,lng),
                  'sensor': 'false'}

    Request = requests.get(URL, params=Parameters)

    jsondata = json.loads(Request.text)

    Result = []
    print(json.dumps(jsondata,indent=4))
    if len(jsondata["results"]) ==0:
        return retrieve_locality(originLatitude,originLongitude, radius)

    result = jsondata["results"][0]

    ac = result["address_components"]
    print(ac)
    if len(ac) < 1:
        return retrieve_locality(originLatitude, originLongitude, radius)

    for component in ac:
        #if 'administrative_area_level_2' in component["types"]:
            #print('>>> %s' % component['short_name'])
            #Result.append(component['short_name'])
        ALLOWED = ['administrative_area_level_1', 'locality']
        for A in ALLOWED:
            if A in component['types']:
                Result.append(component['short_name'])

    if not len(Result) > 1:
        return retrieve_locality(originLatitude,originLongitude, radius)
    Result.append([lat,lng])

    middlelat = (originLatitude - lat)/2
    middlelat = middlelat + lat
    middlelng = (originLongitude - lng)/2
    middlelng = middlelng + lng

    print("Coord Origin: %f,%f   Middle: %f,%f   Destination: %f,%f" %
          (originLatitude,originLongitude,middlelat,middlelng,lat,lng))
    
    Result.append([middlelat, middlelng])
    
    return Result

if __name__ == '__main__':
    W = retrieve_locality(-21.771, -41.35, 0.5)
    print(get_map_image(W[3]))
