from ..parser import ParserContext
from matplotlib.pyplot import imshow
import matplotlib.cm
import numpy


def parse_depth_image(context: ParserContext, snapshot):
    width, height, data = snapshot.image_depth

    path = context.path('depth_image.jpg')

    imshow(numpy.reshape(data, (width, height)), cmap=matplotlib.cm.RdYlGn)
    matplotlib.pyplot.savefig(path)

    # TODO: do this function... Hate matplotlib :(


parse_pose.field = 'depth_image'
