from PIL import Image
import json

from .utils import formatted_encoded_one_data


class ColorImageParser:
    """ A parser that handles probes of "color_image" type. """
    field = 'color_image'

    @staticmethod
    def parse(json_snap_user):
        """ The function that does the parsing
        :param json_snap_user: the data to be parsed.
        :return: the parsed data result.
        """
        try:
            snap_user = json.loads(json_snap_user)
            width, height, data_path, image_path = snap_user["snapshot"]["color_image"]["width"], \
                                                   snap_user["snapshot"]["color_image"]["height"], \
                                                   snap_user["snapshot"]["color_image"]["data_path"], \
                                                   snap_user["snapshot"]["color_image"]["color_image_path"]

            with open(data_path, "rb") as raw_data:
                img_data = raw_data.read()
            image = Image.frombytes('RGB', (width, height), img_data)
            image.save(image_path)

            ret = formatted_encoded_one_data(
                user=snap_user["user"], datetime=snap_user["snapshot"]["datetime"],
                item_key='color_image',
                item_val=dict(width=width, height=height, data_path=data_path, color_image_path=image_path))
            print(f"parser {ColorImageParser.field} finished")
            return ret
        except FileNotFoundError as e:
            print(f"Given data path in snapshot does not exist: {e}")
            raise e
        except Exception as e:
            print(f"parsing color_image failed: {e}")
            raise e
