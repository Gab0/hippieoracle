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


from django.conf import settings


def index(request):
    return showMap(request)
    return HttpResponse("heuhue")


def showMap(request):
    session_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    mapName = 'map_%s.png' % session_name
    dirPath = os.path.join(settings.BASE_DIR,
                           'hippieoracle/hippie/maps/', mapName)

    try:
        W = hippiecore.getCoordinates(-21.771, -41.35, 10, 50)
        IMAGE = hippiecore.get_map_image(W)
        A = hippiecore.downloadMapImage(IMAGE, dirPath)
    except Exception:
        pass

    print(request.META)
    googleUrl = "https://www.google.com/maps/@%f,%f,12z" % (W[0], W[1])
    crosshairPath = os.path.join(settings.BASE_DIR, 'hippieoracle/hippie/sizedtarget.png')
    # processMap.putCrosshair(dirPath, crosshairPath)
    processMap.drawLines(dirPath)
    template = loader.get_template('index.html')
    context = {
        'imagePath': mapName,
        'googleUrl': googleUrl
    }

    return HttpResponse(template.render(context, request))
