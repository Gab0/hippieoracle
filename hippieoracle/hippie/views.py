#!/bin/python
import os
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

import random
import string

from . import hippiecore
from . import processMap
# Create your views here.
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

@csrf_exempt
def index(request):
    template = loader.get_template('distanceSelector.html')
    context = {}
    return HttpResponse(template.render(context, request))

@csrf_exempt
def showMap(request):
    session_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    mapName = 'map_%s.png' % session_name
    hippie_dir = os.path.join(settings.BASE_DIR,
                              'hippieoracle/hippie')

    mapFilePath = os.path.join(hippie_dir, 'maps', mapName)

    print(request.POST)
    minRadius = int(request.POST.get('minDistance'))
    maxRadius = int(request.POST.get('maxDistance'))
    print("Radius:")
    print(minRadius)
    print(maxRadius)

    locations = {
        "Campos": (-21.7587, -41.3267),
        "Rio": (-22.9068, -43.17289)
        }

    LOC = "Campos"
    apipath = os.path.join(settings.BASE_DIR,
                           "hippieoracle/hippie",
                           "google_apikey"
    )

    apikey = list(filter(None, open(apipath).read().split('\n')))[0]
    l = locations[LOC]

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
