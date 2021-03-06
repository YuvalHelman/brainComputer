import numpy
import json
from matplotlib import cm
from matplotlib.pyplot import imshow, savefig

from .utils import formatted_encoded_one_data


class DepthImageParser:
    """ A parser that handles probes of "depth_image" type. """
    field = 'depth_image'

    @staticmethod
    def parse(json_snap_user):
        """ The function that does the parsing
        :param json_snap_user: the data to be parsed.
        :return: the parsed data result.
        """
        try:
            snap_user = json.loads(json_snap_user)
            width, height, data_path, image_path = snap_user["snapshot"]["depth_image"]["width"], \
                                                   snap_user["snapshot"]["depth_image"]["height"], \
                                                   snap_user["snapshot"]["depth_image"]["data_path"], \
                                                   snap_user["snapshot"]["depth_image"]["depth_image_path"],
            with open(data_path, "r") as data:
                str_data = data.read()
            floats_data = [float(x) for x in str_data.split(sep='\n')]
            imshow(numpy.reshape(floats_data, (width, height)), cmap=cm.RdYlGn)
            savefig(image_path)

            ret = formatted_encoded_one_data(
                user=snap_user["user"], datetime=snap_user["snapshot"]["datetime"],
                item_key='depth_image',
                item_val=dict(width=width, height=height, data_path=data_path, depth_image_path=image_path))
            print(f"parser {DepthImageParser.field} finished")
            return ret
        except FileNotFoundError as e:
            print(f"Given data path in snapshot does not exist: {e}")
            raise e
        except Exception as e:
            print(f"parsing depth_image failed: {e}")
            raise e
