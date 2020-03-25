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
    assert res_json["datetime"] == snap_user["snapshot"]["datetime"]
    assert res_json["color_image"]["height"] == snap_user["snapshot"]["color_image"]["height"]
    assert res_json["color_image"]["width"] == snap_user["snapshot"]["color_image"]["width"]
    assert res_json["color_image"]["data_path"] == snap_user["snapshot"]["color_image"]["data_path"]
    assert res_json["color_image"]["color_image_path"] == snap_user["snapshot"]["color_image"]["color_image_path"]

    assert os.path.exists(res_json["color_image"]["color_image_path"]) is True


def test_depth_image_parser_result(encoded_snapshot_user_json_real_data):
    snap_user = json.loads(encoded_snapshot_user_json_real_data)
    assert os.path.exists(snap_user["snapshot"]["depth_image"]["data_path"]) is True

    imageCls = depthImageParser()
    res_json = json.loads(imageCls.parse(encoded_snapshot_user_json_real_data))

    assert res_json["user"]["user_id"] == snap_user["user"]["user_id"]
    assert res_json["user"]["username"] == snap_user["user"]["username"]
    assert res_json["user"]["birthday"] == snap_user["user"]["birthday"]
    assert res_json["user"]["gender"] == snap_user["user"]["gender"]
    assert res_json["datetime"] == snap_user["snapshot"]["datetime"]
    assert res_json["depth_image"]["height"] == snap_user["snapshot"]["depth_image"]["height"]
    assert res_json["depth_image"]["width"] == snap_user["snapshot"]["depth_image"]["width"]
    assert res_json["depth_image"]["data_path"] == snap_user["snapshot"]["depth_image"]["data_path"]
    assert res_json["depth_image"]["depth_image_path"] == snap_user["snapshot"]["depth_image"]["depth_image_path"]

    assert os.path.exists(res_json["depth_image"]["depth_image_path"]) is True


def test_pose_parser_result(encoded_snapshot_user_json_real_data):
    snap_user = json.loads(encoded_snapshot_user_json_real_data)

    parse_func = parse_pose
    res_json = json.loads(parse_func(encoded_snapshot_user_json_real_data))

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


def test_feelings_parser_result(encoded_snapshot_user_json_real_data):
    snap_user = json.loads(encoded_snapshot_user_json_real_data)

    parse_func = parse_feelings
    res_json = json.loads(parse_func(encoded_snapshot_user_json_real_data))

    assert res_json["user"]["user_id"] == snap_user["user"]["user_id"]
    assert res_json["user"]["username"] == snap_user["user"]["username"]
    assert res_json["user"]["birthday"] == snap_user["user"]["birthday"]
    assert res_json["user"]["gender"] == snap_user["user"]["gender"]
    assert res_json["datetime"] == snap_user["snapshot"]["datetime"]
    assert res_json["feelings"]["hunger"] == snap_user["snapshot"]["feelings"]["hunger"]
    assert res_json["feelings"]["thirst"] == snap_user["snapshot"]["feelings"]["thirst"]
    assert res_json["feelings"]["exhaustion"] == snap_user["snapshot"]["feelings"]["exhaustion"]
    assert res_json["feelings"]["happiness"] == snap_user["snapshot"]["feelings"]["happiness"]
