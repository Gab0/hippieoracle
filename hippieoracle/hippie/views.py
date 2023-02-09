#!/bin/python
import os
import random
import string

from django.template import loader
from django.http import HttpResponse

from . import hippiecore
from . import processMap
from . import fetchLocation

# Create your views here.
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


hippie_dir = os.path.join(settings.BASE_DIR,
                          'hippieoracle/hippie')

locationPath = os.path.join(hippie_dir, "locationData.csv")

@csrf_exempt
def index(request):
    template = loader.get_template('distanceSelector.html')

    locationNames = fetchLocation.loadLocations(locationPath).Location
    context = {"locations": locationNames}
    return HttpResponse(template.render(context, request))


@csrf_exempt
def showMap(request):
    session_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    mapName = 'map_%s.png' % session_name

    mapFilePath = os.path.join(hippie_dir, 'maps', mapName)

    print(request.POST)
    minRadius = int(request.POST.get('minDistance'))
    maxRadius = int(request.POST.get('maxDistance'))
    print("Radius:")
    print(minRadius)
    print(maxRadius)


    apipath = os.path.join(settings.BASE_DIR,
                           "hippieoracle/hippie",
                           "google_apikey"
    )

    apikey = list(filter(None, open(apipath).read().split('\n')))[0]

    l = fetchLocation.fetch(request.POST.get("selected_location"), locationPath, apikey)
    l = (l["lat"], l["lng"])

    try:
        W = hippiecore.getCoordinates(l[0], l[1], minRadius, maxRadius)
        IMAGE_URL = hippiecore.get_map_image(W, apikey)
        A = hippiecore.downloadMapImage(IMAGE_URL, mapFilePath)
        reqLogFilePath = os.path.join(hippie_dir, "map_request.log")
        with open(reqLogFilePath, "a+") as reqlog:
            reqlog.write(IMAGE_URL + '\n')
        print(IMAGE_URL)
        print("Downloaded map at %s" % mapFilePath)
    except Exception as e:
        print("MAP DOWNLOAD FAILURE.")
        raise

        pass

    realDistance = hippiecore.calculateRealDistance(l, W)

    # print(request.META)
    googleUrl = "https://www.google.com/maps/@%f,%f,12z" % (W[0], W[1])
    crosshairPath = os.path.join(settings.BASE_DIR, 'hippieoracle/hippie/sizedtarget.png')
    # processMap.putCrosshair(dirPath, crosshairPath)
    processMap.drawLines(mapFilePath)
    template = loader.get_template('mapView.html')
    context = {
        'imagePath': mapName,
        'googleUrl': googleUrl,
        'realDistance': "%.2f" % realDistance
    }

    return HttpResponse(template.render(context, request))
