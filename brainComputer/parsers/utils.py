from pathlib import Path
import inspect
import sys
import importlib
import json


def load_parsers():
    """ loads all of the parsers in the 'parsers' package.
        Uses a dynamic fetch in an aspect oriented manner.
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
    """ returns a 'parser_name' parser using the 'load_parsers' function.
        Throws a KeyError if the parser doesn't exist in the project.
    :param parser_name:
    :return: the function of type 'parser_name'
    """
    parsers_dict = load_parsers()
    return parsers_dict[parser_name]


def formatted_encoded_one_data(user, datetime, item_key, item_val):
    """ Given a single data probe builds the agreed format for json data transfered in the queue """
    return json.dumps(dict(user=user, snapshots={
                                                datetime: {item_key: item_val}
                                                }
                           ))
