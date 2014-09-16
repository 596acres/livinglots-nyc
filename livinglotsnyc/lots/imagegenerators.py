from imagekit import ImageSpec, register
from imagekit.processors import SmartResize


class DetailPageThumbnail(ImageSpec):
    processors = [SmartResize(100, 100)]
    format = 'PNG'
    options = {'quality': 80}

register.generator('lots:detail_page_thumbnail', DetailPageThumbnail)
