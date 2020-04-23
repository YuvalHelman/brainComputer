import pytest
import json

from brainComputer import api


@pytest.fixture(scope='session')
def test_data_path():
    import tests
    return tests.ROOT_DIR + 'data/'


@pytest.fixture(scope='session')
def encoded_snapshot_user_json_real_data(test_data_path):
    """ Json Snapshot example """
    test_snapshot_dir = test_data_path + 'snapshots/42_Dan Gittik/1575446887338/'

    snapshot_user_dict = {"user": {"user_id": 42, "username": "Dan Gittik", "birthday": 699746400, "gender": 0},
                          "snapshot": {"datetime": 1575446887338,
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


@pytest.fixture(scope='session')
def encoded_snapshot_user_json_no_data(test_data_path):
    """ Json Snapshot example without real data for color_image and depth_image"""
    test_snapshot_dir = test_data_path + 'snapshots/42_Dan Gittik/1575446887339/'

    snapshot_user_dict = {"user": {"user_id": 42, "username": "Dan Gittik", "birthday": 699746400, "gender": 0},
                          "snapshot": {"datetime": 1575446887339,
                                       # changed datetime to a different one from encoded_snapshot_user_json_real_data
                                       "pose": {
                                           "translation": {"x": 0.4873843491077423, "y": 0.007090016733855009,
                                                           "z": -1.1306129693984985},
                                           "rotation": {"x": -0.10888676356214629, "y": -0.26755994585035286,
                                                        "z": -0.021271118915446748,
                                                        "w": 0.9571326384559261}},
                                       "color_image": {"width": 0, "height": 0,
                                                       "data_path": test_snapshot_dir + "color_data",
                                                       "color_image_path": test_snapshot_dir + "color_image.png"},
                                       "depth_image": {"width": 0, "height": 0,
                                                       "data_path": test_snapshot_dir + "depth_data",
                                                       "depth_image_path": test_snapshot_dir + "depth_image.png"},
                                       "feelings": {"hunger": 0.0, "thirst": 0.0, "exhaustion": 0.0,
                                                    "happiness": 0.0}}}
    return json.dumps(snapshot_user_dict)


@pytest.fixture(scope='session')
def json_db_document_user43():
    return {'_id': 43, 'user': {'user_id': 43, 'username': 'Dan Gittik', 'birthday': 699746400, 'gender': 0},
            'snapshots': {'1575446887339': {'color_image': {'width': 1920, 'height': 1080,
                                                            'data_path': '/home/user/work/brainComputer/brainComputer/data/42_Dan Gittik/1575446887339/color_data',
                                                            'color_image_path': '/home/user/work/brainComputer/brainComputer/data/42_Dan Gittik/1575446887339/color_image.png'},
                                            'feelings': {'hunger': 0.0, 'thirst': 0.0, 'exhaustion': 0.0,
                                                         'happiness': 0.0}, 'pose': {
                    'translation': {'x': 0.4873843491077423, 'y': 0.007090016733855009, 'z': -1.1306129693984985},
                    'rotation': {'x': -0.10888676356214629, 'y': -0.26755994585035286, 'z': -0.021271118915446748,
                                 'w': 0.9571326384559261}}, 'depth_image': {'width': 224, 'height': 172,
                                                                            'data_path': '/home/user/work/brainComputer/brainComputer/data/42_Dan Gittik/1575446887339/depth_data',
                                                                            'depth_image_path': '/home/user/work/brainComputer/brainComputer/data/42_Dan Gittik/1575446887339/depth_image.png'}},
                          '1575446887412': {'color_image': {'width': 1920, 'height': 1080,
                                                            'data_path': '/home/user/work/brainComputer/brainComputer/data/42_Dan Gittik/1575446887412/color_data',
                                                            'color_image_path': '/home/user/work/brainComputer/brainComputer/data/42_Dan Gittik/1575446887412/color_image.png'},
                                            'pose': {'translation': {'x': 0.15600797533988953, 'y': 0.08133671432733536,
                                                                     'z': -0.49068963527679443},
                                                     'rotation': {'x': -0.2959017411322204, 'y': -0.16749024140672616,
                                                                  'z': -0.04752900380336424, 'w': 0.9392178514199446}},
                                            'feelings': {'hunger': 0.0010000000474974513,
                                                         'thirst': 0.003000000026077032,
                                                         'exhaustion': 0.0020000000949949026, 'happiness': 0.0},
                                            'depth_image': {'width': 224, 'height': 172,
                                                            'data_path': '/home/user/work/brainComputer/brainComputer/data/42_Dan Gittik/1575446887412/depth_data',
                                                            'depth_image_path': '/home/user/work/brainComputer/brainComputer/data/42_Dan Gittik/1575446887412/depth_image.png'}},
                          '1575446887476': {
                              'feelings': {'hunger': 0.0020000000949949026, 'thirst': 0.006000000052154064,
                                           'exhaustion': 0.004000000189989805, 'happiness': 0.0}, 'pose': {
                                  'translation': {'x': -0.05690298229455948, 'y': 0.09136273711919785,
                                                  'z': -0.1454082578420639},
                                  'rotation': {'x': -0.30262250114734884, 'y': 0.024984587319575428,
                                               'z': 0.01379476785565966, 'w': 0.9526831039624887}},
                              'depth_image': {'width': 224, 'height': 172,
                                              'data_path': '/home/user/work/brainComputer/brainComputer/data/42_Dan Gittik/1575446887476/depth_data',
                                              'depth_image_path': '/home/user/work/brainComputer/brainComputer/data/42_Dan Gittik/1575446887476/depth_image.png'},
                              'color_image': {'width': 1920, 'height': 1080,
                                              'data_path': '/home/user/work/brainComputer/brainComputer/data/42_Dan Gittik/1575446887476/color_data',
                                              'color_image_path': '/home/user/work/brainComputer/brainComputer/data/42_Dan Gittik/1575446887476/color_image.png'}}}}


@pytest.fixture(scope='session')
def pb_protocol_user_data():
    return b'\x08*\x12\nDan Gittik\x18\xe0\x90\xd5\xcd\x02'


@pytest.fixture(scope='session')
def pb_protocol_snapshot_data():
    return b'\x08\xab\xf7\xce\xff\xec-\x12C\n\x1b\t\x00\x00\x00 N1\xdf?\x11\x00\x00\x00\xe0k\n}?\x19\x00\x00\x00\xa0\xfd\x16\xf2\xbf\x12$\t\xd5yw\xc0\x00\xe0\xbb\xbf\x11\x1deI\xc0\xb3\x1f\xd1\xbf\x19\xdf[]\xa0\x18\xc8\x95\xbf!\xd1F\x83\xa0\xd4\xa0\xee?\x1a\x00"\x00*\x00'


@pytest.fixture()
def db_mock_mongo(monkeypatch):
    """ Mocks the Mongo Client Class in the db module for testing without the DB on air.
    Works on the function level so other tests can work with the real DB """
    from brainComputer.db import Mongo

    class mockedMongo:
        def __init__(self, url: str):
            pass

        def save(self):
            pass

        def get_users(self):
            return [
                {'user_id': 42, 'username': 'Dan Gittik', 'birthday': 699746400, 'gender': 'm'},
                {'user_id': 43, 'username': 'Yuval Helman', 'birthday': 699746401, 'gender': 'm'},
                {'user_id': 44, 'username': 'Yael Livne', 'birthday': 239746402, 'gender': 'f'},
            ]

        def get_user_id(self, user_id):
            return {'_id': user_id,
                    'user': {'user_id': user_id, 'username': 'usernameMock', 'birthday': 699746400, 'gender': 'm'},
                    'snapshots': {'1575446887339': {'pose': {
                        'translation': {'x': 0.4873843491077423, 'y': 0.007090016733855009, 'z': -1.1306129693984985},
                        'rotation': {'x': -0.10888676356214629, 'y': -0.26755994585035286, 'z': -0.021271118915446748,
                                     'w': 0.9571326384559261}}, 'depth_image': {'width': 224, 'height': 172,
                                                                                'data_path': '/home/user/work/brainComputer/brainComputer/data/42_Dan Gittik/1575446887339/depth_data',
                                                                                'depth_image_path': '/home/user/work/brainComputer/brainComputer/data/42_Dan Gittik/1575446887339/depth_image.png'},
                        'feelings': {'hunger': 0.0, 'thirst': 0.0, 'exhaustion': 0.0,
                                     'happiness': 0.0},
                        'color_image': {'width': 1920, 'height': 1080,
                                        'data_path': '/home/user/work/brainComputer/brainComputer/data/42_Dan Gittik/1575446887339/color_data',
                                        'color_image_path': '/home/user/work/brainComputer/brainComputer/data/42_Dan Gittik/1575446887339/color_image.png'}}}}

    monkeypatch.setattr(Mongo, "__init__", value=mockedMongo.__init__)
    monkeypatch.setattr(Mongo, "save", value=mockedMongo.save)
    monkeypatch.setattr(Mongo, "get_users", value=mockedMongo.get_users)
    monkeypatch.setattr(Mongo, "get_user_id", value=mockedMongo.get_user_id)


@pytest.fixture()
def api_flask_client(db_mock_mongo):
    from brainComputer.db import get_db_handler

    api.app.config['TESTING'] = True
    api.app.config.update(db_handler=get_db_handler('mongodb://127.0.0.1:27017'))
    with api.app.test_client() as client:
        with api.app.app_context():
            yield client
