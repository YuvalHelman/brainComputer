from pathlib import Path
import inspect
import sys
import importlib


def load_parsers():
    """ loads all of the parsers in the parsers/ directory.
    returns: {parser_functionality_string : function_object}
    """
    parsers_dict = {}

    root = Path(__file__).parent.absolute()
    sys.path.insert(0, str(root.parent))
    for path in root.iterdir():
        if path.name.startswith('_') or not path.suffix == '.py':
            continue
        importlib.import_module(f'brainComputer.parsers.{path.stem}')

    parse_modules = [(name, module) for name, module in sys.modules.items() if name.startswith('brainComputer.parsers.')]
    for name, module in parse_modules:
        for objName, callable_obj in module.__dict__.items():
            if inspect.isfunction(callable_obj) and objName.startswith('parse_'):
                parsers_dict[callable_obj.field] = callable_obj
            if inspect.isclass(callable_obj) and objName.endswith('Parser'):
                class_parse_method = getattr(callable_obj, "parse", None)
                if class_parse_method is not None and callable(class_parse_method):
                    parsers_dict[callable_obj.field] = callable_obj.parse
    return parsers_dict


def get_parser_function(parser_name):
    parsers_dict = load_parsers()
    parser_func = parsers_dict[parser_name]
    return parser_func


if __name__ == "__main__":
    print(Path(__file__).parent)
    load_parsers()
