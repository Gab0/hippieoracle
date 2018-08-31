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
    dirPath = os.path.join(settings.BASE_DIR,
                           'hippieoracle/hippie/maps/', mapName)

    print(request.POST)
    minRadius = int(request.POST.get('minDistance'))
    maxRadius = int(request.POST.get('maxDistance'))
    print("Radius:")
    print(minRadius)
    print(maxRadius)

    originLat = -21.771
    originLong = -41.35

    try:
        W = hippiecore.getCoordinates(originLat, originLong, minRadius, maxRadius)
        IMAGE = hippiecore.get_map_image(W)
        A = hippiecore.downloadMapImage(IMAGE, dirPath)
    except Exception as e:
        print(e)
        pass

    realDistance = hippiecore.calculateRealDistance((originLat, originLong), W)

    #print(request.META)
    googleUrl = "https://www.google.com/maps/@%f,%f,12z" % (W[0], W[1])
    crosshairPath = os.path.join(settings.BASE_DIR, 'hippieoracle/hippie/sizedtarget.png')
    # processMap.putCrosshair(dirPath, crosshairPath)
    processMap.drawLines(dirPath)
    template = loader.get_template('mapView.html')
    context = {
        'imagePath': mapName,
        'googleUrl': googleUrl,
        'realDistance': "%.2f" % realDistance
    }

    return HttpResponse(template.render(context, request))
