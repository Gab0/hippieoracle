#!/bin/python
import os
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from . import hippiecore
# Create your views here.

from django.conf import settings


def index(request):
    W = hippiecore.retrieve_locality(-21.771, -41.35, 0.5)
    IMAGE = hippiecore.get_map_image(W[3])
    A = hippiecore.downloadMapImage(IMAGE)

    template = loader.get_template('index.html')
    context = {'imagePath': 'MAP.png'}
    # return HttpResponse("<img src='%s'>" % IMAGE)
    return HttpResponse(template.render(context, request))
