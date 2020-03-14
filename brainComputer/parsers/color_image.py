from pathlib import Path
from PIL import Image
import json
from brainComputer.utils import get_saving_path


class colorImageParser:
    field = 'color_image'

    def parse(self, json_snap_user):
        snap_user = json.loads(json_snap_user)
        width, height, data_path = snap_user["snapshot"]["color_image"]["width"], \
                                   snap_user["snapshot"]["color_image"]["height"], \
                                   snap_user["snapshot"]["color_image"]["data_path"],
        with open(data_path, "rb") as fd:
            data = fd.read(width * height)
            image = Image.frombytes('RGB', (width, height), data)
        data_dir = get_saving_path(snap_user["user"], snap_user["snapshot"], is_proto=False)
        color_path = data_dir / "color_image"
        image.save(color_path)

        return json.dumps(dict(
            width=width,
            height=height,
            data_path=data_path,
            image=color_path, # TODO: add user and timestamp
        )

                          )
# @Parser.parser('color_image')
# def parse_color_image(context, snapshot):
#     p = Path(f"{context.parser_path}/color_image.json")
#     width, height, data = snapshot.color_image
#     image = Image.frombytes('RGB', (width, height), data)
#
#     with open(p, mode="w") as fd:
#         image.save(p)
