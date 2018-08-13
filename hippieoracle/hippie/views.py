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
    W = hippiecore.retrieve_locality(-21.771, -41.35, 0.5)
    IMAGE = hippiecore.get_map_image(W[3])

    dirPath = os.path.join(settings.BASE_DIR, 'hippieoracle/hippie/maps/MAP.png')
    A = hippiecore.downloadMapImage(IMAGE, dirPath)

    crosshairPath = os.path.join(settings.BASE_DIR, 'hippieoracle/hippie/sizedtarget.png')
    processMap.putCrosshair(dirPath, crosshairPath)
    template = loader.get_template('index.html')
    context = {'imagePath': 'MAP.png'}

    return HttpResponse(template.render(context, request))
