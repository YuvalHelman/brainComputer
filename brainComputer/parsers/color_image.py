from pathlib import Path
from PIL import Image
import json


class colorImageParser:
    field = 'color_image'

    def parse(self, json_snap_user):
        snap_user = json.loads(json_snap_user)


        image = Image.frombytes('RGB', (width, height), data)

        image.save(path)
        # TODO: save the image itself to a path.

# @Parser.parser('color_image')
# def parse_color_image(context, snapshot):
#     p = Path(f"{context.parser_path}/color_image.json")
#     width, height, data = snapshot.color_image
#     image = Image.frombytes('RGB', (width, height), data)
#
#     with open(p, mode="w") as fd:
#         image.save(p)
