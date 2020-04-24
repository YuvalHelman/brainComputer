from .utils import get_parser_function, load_parsers


def run_parser(parser_name, data):
    """  accepts a parser name and some raw data, as consumed from the message queue, and returns the result
    :param parser_name: the name of the parser's functionality
    :param data: the data to be parsed
    :return: the parsed result
    """
    try:
        parser_func = get_parser_function(parser_name)
        return parser_func(data)
    except KeyError as e:
        print(f"{parser_name} isn't a valid parser name")
        return 1
    except Exception as e:
        print(f"run_parser {parser_name} failed: {e}")
        return 1
