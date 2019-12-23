from pathlib import Path
import json
from ..parser import ParserContext


def parse_pose(context: ParserContext, snapshot):
    x, y, z = snapshot.translation
    a, b, c, d = snapshot.rotation

    context.save('pose.json',
                 (json.dumps({'translation': {"x": x, "y": y, "z": z},
                              'rotation': {"x": a, "y": b, "z": c, "w": d}
                              })
                  ))


parse_pose.field = 'pose'
