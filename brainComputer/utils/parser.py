import datetime
from pathlib import Path
import inspect
from .parsers import __init__ as parsers


class Parser:
    """
    Parser is being used as a container. it's the "context" argument that's being passed to the
    parse functions. also it collects all of the parses from the 'parses' package.
    """

    def __init__(self, dir_path, hello, snapshot):
        self.dir_path = dir_path
        self.fields_dict = {}

        for name, object in inspect.getmembers(parsers):
            if inspect.isfunction(object) and name.startswith('parse'):
                self.fields_dict[object.field] = object
                # print(name, object)  # DEBUG
                # print(object.field)  # DEBUG
            if inspect.isclass(object) and name.endswith('Parser'):
                self.fields_dict[object.field] = object.parse
                # print(name, object)  # DEBUG
                # print(object.field)  # DEBUG
        print(self.fields_dict)

        try:
            self.parser_path = self.get_path_for_storage(hello, snapshot)
        except Exception as e:
            self.parser_path = None

    def get_path_for_storage(self, hello, snapshot):
        timestamp = snapshot.timestamp
        user_id = hello.user.id
        timeString = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d_%H-%M-%S')
        p_dir = Path(f"{self.dir_path}{user_id}/{timeString}")

        if not p_dir.exists():
            p_dir.mkdir(parents=True, exist_ok=True)

        return p_dir


if __name__ == "__main__":
    p = Parser(None, None, None)
