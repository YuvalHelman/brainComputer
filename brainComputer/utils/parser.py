import datetime
from pathlib import Path
import inspect
import .parsers


class Parser:
    """
    Parser is being used as a container. it's the "context" argument that's being passed to the
    parse functions. also it collects all of the parses from the 'parses' package.
    """

    def __init__(self, dir_path, hello, snapshot):
        self.dir_path = dir_path
        self.parser_path = None
        self.fields_dict = {}

        for name, object in inspect.getmembers(parsers):
            if inspect.isfunction(object) and name.startswith('parse'):
                self.fields_dict[object.field] = object
            if inspect.isclass(object) and name.endswith('Parser'):
                self.fields_dict[object.field] = object.parse
        print(self.fields_dict)

        self.parser_path = self.build_snapshot_dir_path(hello, snapshot)

    def build_snapshot_dir_path(self, hello, snapshot):
        timestamp = snapshot.timestamp
        user_id = hello.user.id
        timeString = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d_%H-%M-%S')
        p_dir = Path(f"{self.dir_path}{user_id}/{timeString}")

        if not p_dir.exists():
            p_dir.mkdir(parents=True, exist_ok=True)

        return p_dir

    def path(self, field_name: str):
        return self.parser_path / field_name

    def save(self, snapshot):
        pass


if __name__ == "__main__":
    p = Parser("/tmp/", None, None)
    p.path('color_image')
