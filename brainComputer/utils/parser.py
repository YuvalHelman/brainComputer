import datetime
from pathlib import Path
import inspect
import sys
import importlib


class ParserContext:
    """
    This is the "context" argument that's being passed to the parse functions.
    """

    def __init__(self, dir_path, user_id, snapshot):
        self.dir_path = dir_path

        try:
            self.parser_path = self.build_snapshot_dir_path(user_id, snapshot.timestamp)
        except Exception as e:
            print('Creating context Object failed.', e)

    def build_snapshot_dir_path(self, user_id, timestamp):
        timeString = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d_%H-%M-%S')
        p_dir = Path(f"{self.dir_path}{user_id}/{timeString}")

        if not p_dir.exists():
            p_dir.mkdir(parents=True, exist_ok=True)

        return p_dir

    def path(self, field_name: str):
        return self.parser_path / field_name

    def save(self, field_name: str, what_to_write: str):
        with open(self.path(field_name), mode="w") as fd:
            fd.write(what_to_write)


class Parsers:
    """
    Parser is being used as a container for all parsers that were defines in the parsers/ submodule.
    It also collects all of the parses from the 'parses' package.
    """
    root = Path(__file__).parent.joinpath('parsers')

    @classmethod
    def load_modules(cls):
        """ loads all of the modules in the parsers/ submodule and returns them as a dictionary of
        {parser_functionality_string : function_object} """
        root = Parsers.root
        parsers_dict = {}
        root = Path(root).absolute()
        sys.path.insert(0, str(root.parent))
        for path in root.iterdir():
            if path.name.startswith('_') or not path.suffix == '.py':
                continue
            importlib.import_module(f'brainComputer.utils.parsers.{path.stem}')

        for name, module in sys.modules.items():
            if name.startswith('parsers.'):
                for objName, callable_obj in module.__dict__.items():
                    if inspect.isfunction(callable_obj) and objName.startswith('parse'):
                        parsers_dict[callable_obj.field] = callable_obj
                    if inspect.isclass(callable_obj) and objName.endswith('Parser'):
                        class_parse_method = getattr(callable_obj, "parse", None)
                        if class_parse_method is not None and callable(class_parse_method):
                            parsers_dict[callable_obj.field] = callable_obj.parse
        return parsers_dict


if __name__ == "__main__":
    print(Parsers.root)
    Parsers.load_modules()

