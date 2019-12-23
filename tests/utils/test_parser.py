import pytest

from brainComputer.utils.parser import Parsers, ParserContext


@pytest.fixture
def a():
    return 'Hey'  # TODO: see if this is useful


def test_load_modules():
    pass
    # Mock the "Parsers.root" variable to some Temp Dir, create files there,
    # and check if it compiles as expected
    old_root = Parsers.root
    Parsers.root = "SOME_TEMP_DIR"  # TODO: add some kind of directory
    #  --------------------
    #   TODO
    #  -------------------
    Parsers.root = old_root


if __name__ == "__main__":
    test_load_modules()
