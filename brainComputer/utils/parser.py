import functools
import datetime
from pathlib import Path
from PIL import Image
import json
import inspect
import parsers


class Parser:
    """
    Parser is being used as a container. it's the "context" argument that's being passed to the
    parse functions. also it contains the function that decorates these functions.
    """
    fields_dict = {}

    def __init__(self, dir_path, hello, snapshot):
        self.dir_path = dir_path
        try:
            self.parser_path = self.get_path_for_storage(hello, snapshot)
        except Exception as e:
            self.parser_path = None

    @classmethod
    def parser(cls, field_name):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            Parser.fields_dict[field_name] = func

            return wrapper

        return decorator
        # TODO: maybe need a wrapper here?

    def get_path_for_storage(self, hello, snapshot):
        timestamp = snapshot.timestamp
        user_id = hello.user.id
        timeString = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d_%H-%M-%S')
        p_dir = Path(f"{self.dir_path}{user_id}/{timeString}")

        if not p_dir.exists():
            p_dir.mkdir(parents=True, exist_ok=True)

        return p_dir


# @Parser.parser('color_image')
# def parse_color_image(context, snapshot):
#     p = Path(f"{context.parser_path}/color_image.json")
#     width, height, data = snapshot.color_image
#     image = Image.frombytes('RGB', (width, height), data)
#
#     with open(p, mode="w") as fd:
#         image.save(p)
#
#
# @Parser.parser('translation')
# def parse_translation(context, snapshot):
#     p = Path(f"{context.parser_path}/translation.json")
#     x, y, z = snapshot.translation
#
#     with open(p, mode="w") as fd:
#         fd.write(json.dumps({"x": x, "y": y, "z": z}))


if __name__ == "__main__":
    p = Parser(None, None, None)
    # print(p.fields_dict)
    # print(dir())
    for first, second in inspect.getmembers(parsers):
        print(first, second)
        if first == 'parse_color_image':
            print(second.field)
