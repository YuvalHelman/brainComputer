import json
import pytest
import random
import string
from brainComputer.parsers import run_parser, load_parsers


def test_run_parser_works(snapshot_user_json_encoded):
    # GIVEN pose builtin parser
    snap_user = json.loads(snapshot_user_json_encoded)
    # WHEN running a parser from run_parser
    res = run_parser('pose', snapshot_user_json_encoded)
    # THEN returned an encoded json appropriate to the pose_parse function
    res_json = json.loads(res)
    assert res_json["user"]["user_id"] == snap_user["user"]["user_id"]
    assert res_json["user"]["username"] == snap_user["user"]["username"]
    assert res_json["user"]["birthday"] == snap_user["user"]["birthday"]
    assert res_json["user"]["gender"] == snap_user["user"]["gender"]
    assert res_json["datetime"] == snap_user["snapshot"]["datetime"]
    assert res_json["pose"]["translation"]["x"] == snap_user["snapshot"]["pose"]["translation"]["x"]
    assert res_json["pose"]["translation"]["y"] == snap_user["snapshot"]["pose"]["translation"]["y"]
    assert res_json["pose"]["translation"]["z"] == snap_user["snapshot"]["pose"]["translation"]["z"]
    assert res_json["pose"]["rotation"]["x"] == snap_user["snapshot"]["pose"]["rotation"]["x"]
    assert res_json["pose"]["rotation"]["y"] == snap_user["snapshot"]["pose"]["rotation"]["y"]
    assert res_json["pose"]["rotation"]["z"] == snap_user["snapshot"]["pose"]["rotation"]["z"]
    assert res_json["pose"]["rotation"]["w"] == snap_user["snapshot"]["pose"]["rotation"]["w"]


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
