import json
import pytest
import random
import string
from brainComputer.parsers import run_parser, load_parsers


def test_run_parser_works(encoded_snapshot_user_json_real_data):
    """ check that loading a parser works """
    # GIVEN pose builtin parser
    snap_user = json.loads(encoded_snapshot_user_json_real_data)
    # WHEN loading a parser from run_parser
    res = run_parser('pose', encoded_snapshot_user_json_real_data)
    # THEN returned json matches the expected.
    res_json = json.loads(res)
    assert res_json["user"]["user_id"] == snap_user["user"]["user_id"]
    assert res_json["user"]["username"] == snap_user["user"]["username"]
    assert res_json["user"]["birthday"] == snap_user["user"]["birthday"]
    assert res_json["user"]["gender"] == snap_user["user"]["gender"]
    assert res_json["snapshots"][0]["pose"] == snap_user["snapshot"]["pose"]


def test_run_parser_throws(capsys):
    parsers_dict = load_parsers()
    parser_name = random_string_generator()
    if parser_name in parsers_dict:
        return
    with pytest.raises(KeyError):
        parser_func = parsers_dict[parser_name]
        out, err = capsys.readouterr()
        assert out == f"{parser_name} isn't a valid parser name"


def random_string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
