"""
Script:     Catalogger App
Developer:  Dave Whitehouse - D2IQ Solutions Architect
Contact:    @dwhitehouse
Date:       7 Oct 22
Summary:    Builds a mini thumbnail gallery of all icons uploaded
"""

from os import listdir
from os.path import isfile, join
import base64

def build_gallery(folder):
    gallery = ""
    for image in listdir(folder):
        if not image == '.gitkeep':
            name = image.split('.')[0]
            gallery = gallery + f"<img style=\"width: 27px;height: 27px;margin-left: 10px\" src=\"assets/icons/{image}\" alt=\"{name}\"/>"
    return gallery
