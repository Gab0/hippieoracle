#!/bin/python
from PIL import Image


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
