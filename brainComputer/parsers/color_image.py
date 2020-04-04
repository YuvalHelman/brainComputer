from PIL import Image
import json

from brainComputer.utils import formatted_encoded_one_data


class colorImageParser:
    field = 'color_image'

    @staticmethod
    def parse(json_snap_user):
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
            print(f"parser {colorImageParser.field} finished")
            return ret
        except FileNotFoundError as e:
            print(f"Given data path in snapshot does not exist: {e}")
            raise e
        except Exception as e:
            print(f"parsing color_image failed: {e}")
            raise e
