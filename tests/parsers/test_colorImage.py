import pytest
from PIL import Image
from brainComputer.parsers.color_image import colorImageParser
import json


@pytest.fixture()
def snapshot():
    """ Json Snapshot example """
    test_snapshot_dir = "/home/user/work/brainComputer/tests/snapshots/42_Dan Gittik/1575446887339/"
    return json.dumps(
        {"user": {"user_id": 42, "username": "Dan Gittik", "birthday": 699746400, "gender": 0},
         "snapshot": {"datetime": 1575446887339,
                      "pose": {
                          "translation": {"x": 0.4873843491077423, "y": 0.007090016733855009, "z": -1.1306129693984985},
                          "rotation": {"x": -0.10888676356214629, "y": -0.26755994585035286, "z": -0.021271118915446748,
                                       "w": 0.9571326384559261}},
                      "color_image": {"width": 1920, "height": 1080,
                                      "data_path": test_snapshot_dir + "color_data",
                                      "color_image_path": test_snapshot_dir + "color_image"},
                      "depth_image": {"width": 224, "height": 172,
                                      "data_path": test_snapshot_dir + "depth_data",
                                      "depth_image_path": test_snapshot_dir + "depth_image"},
                      "feelings": {"hunger": 0.0, "thirst": 0.0, "exhaustion": 0.0, "happiness": 0.0}}}
    )


def test_colorImageParserResult(snapshot):
    imageCls = colorImageParser()
    res_json = json.loads(imageCls.parse(snapshot))
    assert res_json["user"]["user_id"] == snapshot["snapshot"]["user"]["user_id"]
    assert res_json["user"]["username"] == snapshot["snapshot"]["user"]["username"]
    assert res_json["user"]["birthday"] == snapshot["snapshot"]["user"]["birthday"]
    assert res_json["user"]["gender"] == snapshot["snapshot"]["user"]["gender"]
    assert res_json["datetime"] == snapshot["snapshot"]["datetime"]
    assert res_json["color_image"]["height"] == snapshot["snapshot"]["color_image"]["height"]
    assert res_json["color_image"]["width"] == snapshot["snapshot"]["color_image"]["width"]
    assert res_json["color_image"]["data_path"] == snapshot["snapshot"]["color_image"]["data_path"]
    assert res_json["color_image"]["color_image"] == snapshot["snapshot"]["color_image"]["data_path"]

    #
    # myimage = Image.open(res_json[""])
    # myimage.load()
    return 0
# user=snap_user["user"],
#             datetime=snap_user["snapshot"]["datetime"],
#             width=width,
#             height=height,
#             data_path=data_path,
#             image=color_image_path,
