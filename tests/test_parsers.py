import pytest
import os
from brainComputer.parsers.color_image import colorImageParser
from brainComputer.parsers.depth_image import depthImageParser
import json


@pytest.fixture()
def snapshot_user_encoded():
    """ Json Snapshot example """
    test_snapshot_dir = "/tests/snapshots/42_Dan Gittik/1575446887339/"
    return json.dumps(
        {"user": {"user_id": 42, "username": "Dan Gittik", "birthday": 699746400, "gender": 0},
         "snapshot": {"datetime": 1575446887339,
                      "pose": {
                          "translation": {"x": 0.4873843491077423, "y": 0.007090016733855009, "z": -1.1306129693984985},
                          "rotation": {"x": -0.10888676356214629, "y": -0.26755994585035286, "z": -0.021271118915446748,
                                       "w": 0.9571326384559261}},
                      "color_image": {"width": 1920, "height": 1080,
                                      "data_path": test_snapshot_dir + "color_data",
                                      "color_image_path": test_snapshot_dir + "color_image.png"},
                      "depth_image": {"width": 224, "height": 172,
                                      "data_path": test_snapshot_dir + "depth_data",
                                      "depth_image_path": test_snapshot_dir + "depth_image.png"},
                      "feelings": {"hunger": 0.0, "thirst": 0.0, "exhaustion": 0.0, "happiness": 0.0}}}
    )


def test_color_image_parser_result(snapshot_user_encoded):
    snap_user = json.loads(snapshot_user_encoded)

    imageCls = colorImageParser()
    res_json = json.loads(imageCls.parse(snapshot_user_encoded))

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


def test_depth_image_parser_result(snapshot_user_encoded):
    snap_user = json.loads(snapshot_user_encoded)

    imageCls = depthImageParser()
    res_json = json.loads(imageCls.parse(snapshot_user_encoded))

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
