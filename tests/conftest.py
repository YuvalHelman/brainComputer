import pytest
import json


@pytest.fixture()
def snapshot_user_json_encoded():
    """ Json Snapshot example """
    test_snapshot_dir = "tests/snapshots/42_Dan Gittik/1575446887339/"

    snapshot_user_dict = {"user": {"user_id": 42, "username": "Dan Gittik", "birthday": 699746400, "gender": 0},
                          "snapshot": {"datetime": 1575446887339,
                                       "pose": {
                                           "translation": {"x": 0.4873843491077423, "y": 0.007090016733855009,
                                                           "z": -1.1306129693984985},
                                           "rotation": {"x": -0.10888676356214629, "y": -0.26755994585035286,
                                                        "z": -0.021271118915446748,
                                                        "w": 0.9571326384559261}},
                                       "color_image": {"width": 1920, "height": 1080,
                                                       "data_path": test_snapshot_dir + "color_data",
                                                       "color_image_path": test_snapshot_dir + "color_image.png"},
                                       "depth_image": {"width": 224, "height": 172,
                                                       "data_path": test_snapshot_dir + "depth_data",
                                                       "depth_image_path": test_snapshot_dir + "depth_image.png"},
                                       "feelings": {"hunger": 0.0, "thirst": 0.0, "exhaustion": 0.0, "happiness": 0.0}}}

    return json.dumps(snapshot_user_dict)
