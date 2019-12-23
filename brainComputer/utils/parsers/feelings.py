from pathlib import Path
import json
from ..parser import ParserContext


def parse_pose(context: ParserContext, snapshot):
    hunger, thirst, exhaustion, happiness = snapshot.feelings

    context.save('feelings.json',
                 json.dumps({'feelings': {"hunger": hunger, "thirst": thirst,
                                          "exhaustion": exhaustion, "happiness": happiness},
                             })
                 )


parse_pose.field = 'feelings'
