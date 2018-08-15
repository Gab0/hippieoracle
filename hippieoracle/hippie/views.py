#!/bin/python
import os
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from . import hippiecore
from . import processMap
# Create your views here.


from django.conf import settings


def index(request):
    dirPath = os.path.join(settings.BASE_DIR, 'hippieoracle/hippie/maps/MAP.png')
    try:
        W = hippiecore.getCoordinates(-21.771, -41.35, 0.1, 0.3)
        IMAGE = hippiecore.get_map_image(W)
        A = hippiecore.downloadMapImage(IMAGE, dirPath)
    except Exception:
        pass

    crosshairPath = os.path.join(settings.BASE_DIR, 'hippieoracle/hippie/sizedtarget.png')
    # processMap.putCrosshair(dirPath, crosshairPath)
    processMap.drawLines(dirPath)
    template = loader.get_template('index.html')
    context = {'imagePath': 'MAP.png'}

    return HttpResponse(template.render(context, request))
