from .utils import get_parser_function


def run_parser(parser_name, data):
    try:
        parser_func = get_parser_function(parser_name)
        return parser_func(data)
    except KeyError as e:
        print(f"{parser_name} isn't a valid parser name")
        return 1
    except Exception as e:
        print(f"run_parser {parser_name} failed: {e}")
        return 1

