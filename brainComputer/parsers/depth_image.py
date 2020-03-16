import matplotlib.cm
import numpy
import json
from brainComputer.utils import get_saving_path


class depthImageParser:
    field = 'depth_image'

    def parse(self, json_snap_user):
        snap_user = json.loads(json_snap_user)

        width, height, data_path = snap_user["snapshot"]["color_image"]["width"], \
                                   snap_user["snapshot"]["color_image"]["height"], \
                                   snap_user["snapshot"]["color_image"]["data_path"],
        with open(data_path, "rb") as fd:
            data = fd.read(width * height * 3)
            image = Image.frombytes('RGB', (width, height), data)

        data_dir = get_saving_path(snap_user["user"], snap_user["snapshot"], is_proto=False)
        color_image_path = data_dir / "color_image"
        with open(color_image_path, 'w'):
            image.save(color_image_path)

        return json.dumps(dict(
            user=snap_user["user"],
            datetime=snap_user["snapshot"]["datetime"],
            width=width,
            height=height,
            data_path=data_path,
            image=color_image_path,
        ))
