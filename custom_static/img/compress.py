from glob import glob
from os.path import splitext
from PIL import Image

jpglist = glob( "*.[jJ][pP][gG]" )

for jpg in jpglist:
    im = Image.open(jpg)
    png = splitext(jpg)[0]+ splitext(jpg)[1]

    im.save(png, quality=85, optimize=True)
