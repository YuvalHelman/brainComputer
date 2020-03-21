from .utils import load_parsers


def run_parser(parser_name, data):
    try:
        parsers_dict = load_parsers()
        parser_func = parsers_dict[parser_name]
        return parser_func(data)
    except KeyError as e:
        print(f"{parser_name} isn't a valid parser name")
        return 1
    except Exception as e:
        print(f"run_parser failed: {e}")
        return 1
