from imagekit import ImageSpec, register
from imagekit.processors import SmartResize


class Thumbnail(ImageSpec):
    processors = [SmartResize(600, 400)]
    format = 'PNG'
    options = {'quality': 80}

register.generator('cms:thumbnail', Thumbnail)
