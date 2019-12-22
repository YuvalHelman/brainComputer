import datetime
from pathlib import Path
import inspect
import sys
import importlib


class Parser:
    """
    Parser is being used as a container. it's the "context" argument that's being passed to the
    parse functions. also it collects all of the parses from the 'parses' package.
    """

    def __init__(self, dir_path, hello, snapshot):
        self.dir_path = dir_path
        self.parser_path = None
        self.fields_dict = {}

        self.load_modules(Path(__file__).parent.joinpath('parsers'))

        #

        # TODO: get this back from the dead
        # self.parser_path = self.build_snapshot_dir_path(hello, snapshot)

    # def load_parsers(self):

    def load_modules(self, root):
        root = Path(root).absolute()
        sys.path.insert(0, str(root.parent))
        for path in root.iterdir():
            if path.name.startswith('_') or not path.suffix == '.py':
                continue
            importlib.import_module(f'{root.name}.{path.stem}', package=root.name)

        for name, module in sys.modules.items():
            if name.startswith('parsers.'):
                for objName, callable_obj in module.__dict__.items():
                    if inspect.isfunction(callable_obj) and objName.startswith('parse'):
                        self.fields_dict[callable_obj.field] = callable_obj
                    if inspect.isclass(callable_obj) and objName.endswith('Parser'):
                        class_parse_method = getattr(callable_obj, "parse", None)
                        if class_parse_method is not None and callable(class_parse_method):
                            self.fields_dict[callable_obj.field] = callable_obj.parse

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
    print(p.fields_dict)

