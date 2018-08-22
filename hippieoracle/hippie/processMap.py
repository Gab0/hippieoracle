#!/bin/python
from PIL import Image


def drawLines(mapFilename):
    mapImage = Image.open(mapFilename)

    mapPixels = mapImage.load()

    height, width = mapImage.size

    def makeLines(length, linecount=2):
        lines = [length // (linecount + 1) * (z+1) for z in range(linecount)]
        return lines

    verticalLinePoints = makeLines(height)
    horizontalLinePoints = makeLines(width)
    for v in range(height):
        for h in range(width):
            if v in verticalLinePoints:
                if not h % 3:
                    mapPixels[v, h] = 0
            if h in horizontalLinePoints:
                if not v % 3:
                    mapPixels[v, h] = 0

    mapImage.save(mapFilename)


def putCrosshair(mapFilename, crosshairFilename, resize=True):

    # Usage:
    mapImage = Image.open(mapFilename)
    crosshairImage = Image.open(crosshairFilename)
    # newimg = PasteImage(srcimg, tgtimg, (5, 5))
    # newimg.save('some_new_image.png')
    #

    if resize:
        cH, cW = crosshairImage.size
        crosshairImage = crosshairImage.resize((int(cH * 1.60),
                                                int(cW * 1.60)),
                                               Image.ANTIALIAS)
    mH, mW = mapImage.size
    cH, cW = crosshairImage.size

    middleH = int(mH / 2 - cH / 2)
    middleW = int(mW / 2 - cW / 2)
    #crosshairImage.paste(mapImage, (4,4))
    mapImage.paste(crosshairImage, (middleH, middleW), crosshairImage)
    #mapImage.show()
    mapImage.save(mapFilename)
