from brainComputer.utils.parser import ParserContext
from matplotlib.pyplot import imshow
import matplotlib.cm
import numpy


def parse_depth_image(context: ParserContext, snapshot):
    width, height, data = snapshot.image_depth

    path = context.path('depth_image.jpg')

    # TODO: do this function... Hate matplotlib :(


parse_depth_image.field = 'depth_image'
