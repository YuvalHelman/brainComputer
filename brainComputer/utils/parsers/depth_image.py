from pathlib import Path
import json
from ..parser import ParserContext
from matplotlib.pyplot import imshow
import matplotlib.cm

def parse_pose(context: ParserContext, snapshot):
    hunger, thirst, exhaustion, happiness = snapshot.feelings

    context.save('feelings.json',
                 json.dumps({'feelings': {"hunger": hunger, "thirst": thirst,
                                          "exhaustion": exhaustion, "happiness": happiness},
                             })
                 )

    width, height, data = snapshot.image_depth
    path = f'{self.get_path(user_id, snapshot.timestamp)}/depth_image.jpg'
    imshow(numpy.reshape(data, (width, height)), cmap=matplotlib.cm.RdYlGn)
    matplotlib.pyplot.savefig(path)


parse_pose.field = 'feelings'


