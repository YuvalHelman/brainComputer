import pytest
import os
import json

from brainComputer.parsers.color_image import colorImageParser
from brainComputer.parsers.depth_image import depthImageParser
from brainComputer.parsers.pose import parse_pose
from brainComputer.parsers.feelings import parse_feelings


def test_color_image_parser_result(encoded_snapshot_user_json_real_data):
    snap_user = json.loads(encoded_snapshot_user_json_real_data)
    assert os.path.exists(snap_user["snapshot"]["color_image"]["data_path"]) is True

    imageCls = colorImageParser()
    res_json = json.loads(imageCls.parse(encoded_snapshot_user_json_real_data))

    assert res_json["user"]["user_id"] == snap_user["user"]["user_id"]
    assert res_json["user"]["username"] == snap_user["user"]["username"]
    assert res_json["user"]["birthday"] == snap_user["user"]["birthday"]
    assert res_json["user"]["gender"] == snap_user["user"]["gender"]

    res_datetime_val = list(res_json["snapshots"].keys())[0]
    assert int(res_datetime_val) == snap_user["snapshot"]["datetime"]
    assert res_json["snapshots"][res_datetime_val]['color_image'] == snap_user["snapshot"]["color_image"]

    assert os.path.exists(res_json["snapshots"][res_datetime_val]['color_image']["color_image_path"]) is True


def test_depth_image_parser_result(encoded_snapshot_user_json_real_data):
    snap_user = json.loads(encoded_snapshot_user_json_real_data)
    assert os.path.exists(snap_user["snapshot"]["depth_image"]["data_path"]) is True

    imageCls = depthImageParser()
    res_json = json.loads(imageCls.parse(encoded_snapshot_user_json_real_data))

    assert res_json["user"]["user_id"] == snap_user["user"]["user_id"]
    assert res_json["user"]["username"] == snap_user["user"]["username"]
    assert res_json["user"]["birthday"] == snap_user["user"]["birthday"]
    assert res_json["user"]["gender"] == snap_user["user"]["gender"]
    res_datetime_val = list(res_json["snapshots"].keys())[0]
    assert int(res_datetime_val) == snap_user["snapshot"]["datetime"]
    assert res_json["snapshots"][res_datetime_val]['depth_image'] == snap_user["snapshot"]["depth_image"]
    assert os.path.exists(res_json["snapshots"][res_datetime_val]['depth_image']["depth_image_path"]) is True


def test_pose_parser_result(encoded_snapshot_user_json_real_data):
    # GIVEN pose builtin parser
    # WHEN running a parser from run_parser
    # THEN returned an encoded json appropriate to the pose_parse function
    snap_user = json.loads(encoded_snapshot_user_json_real_data)

    parse_func = parse_pose
    res_json = json.loads(parse_func(encoded_snapshot_user_json_real_data))

    assert res_json["user"]["user_id"] == snap_user["user"]["user_id"]
    assert res_json["user"]["username"] == snap_user["user"]["username"]
    assert res_json["user"]["birthday"] == snap_user["user"]["birthday"]
    assert res_json["user"]["gender"] == snap_user["user"]["gender"]
    res_datetime_val = list(res_json["snapshots"].keys())[0]
    assert int(res_datetime_val) == snap_user["snapshot"]["datetime"]
    assert res_json["snapshots"][res_datetime_val]['pose'] == snap_user["snapshot"]["pose"]


def test_feelings_parser_result(encoded_snapshot_user_json_real_data):
    snap_user = json.loads(encoded_snapshot_user_json_real_data)

    parse_func = parse_feelings
    res_json = json.loads(parse_func(encoded_snapshot_user_json_real_data))

    assert res_json["user"]["user_id"] == snap_user["user"]["user_id"]
    assert res_json["user"]["username"] == snap_user["user"]["username"]
    assert res_json["user"]["birthday"] == snap_user["user"]["birthday"]
    assert res_json["user"]["gender"] == snap_user["user"]["gender"]

    res_datetime_val = list(res_json["snapshots"].keys())[0]
    assert int(res_datetime_val) == snap_user["snapshot"]["datetime"]
    assert res_json["snapshots"][res_datetime_val]['feelings'] == snap_user["snapshot"]["feelings"]
