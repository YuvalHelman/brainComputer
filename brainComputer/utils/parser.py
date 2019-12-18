import functools
import datetime
from pathlib import Path
from PIL import Image

class Parser:
    fields_dict = {}
    @classmethod
    def parser(cls, field_name):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):

                Parser.fields_dict[field_name] = func

            return wrapper

        return decorator

    def create_path(self, timestamp):
        timeString = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d_%H-%M-%S')
        p_dir = Path(f"{self.data_dir}{user_id}/{timeString}")

        if not p_dir.exists():
            p_dir.mkdir(parents=True, exist_ok=True)


@Parser.parser('color_image')
def parse_color_image(snapshot, user):
    pass

@Parser.parser('color_image')
    def parse_translation():
    pass


def write_fields_to_file(self, user_id, timestamp, translation, color_image):
    """ the server saves the thought into:
    data/user_id/datetime/translation.json
    With the following JSON format: {"x": x, "y": y, "z": z}.
    """


    p1 = Path(f"{p_dir}/translation.json")
    p2 = Path(f"{p_dir}/color_image.json")
    x, y, z = translation
    width, height, data = color_image
    image = Image.frombytes('RGB', (width, height), data)


    with open(p1, mode="w") as fd:
        fd.write(json.dumps({"x": x, "y": y, "z": z}))
    with open(p2, mode="w") as fd:
        image.save(p2)