import pytest
from brainComputer import api


@pytest.fixture()
def api_flask_client(db_mock_mongo):
    from brainComputer.db import get_db_handler

    api.app.config['TESTING'] = True
    api.app.config.update(db_handler=get_db_handler('mongodb://127.0.0.1:27017'))
    with api.app.test_client() as client:
        with api.app.app_context():
            yield client


def test_api_users(api_flask_client):
    resp = api_flask_client.get('http://127.0.0.1:5000/users')
    assert resp.data == b'{"42":"Dan Gittik","43":"Yuval Helman","44":"Yael Livne"}\n'
    assert resp.status_code == 200


def test_api_get_user_id(api_flask_client):
    resp = api_flask_client.get('http://127.0.0.1:5000/users/42')
    assert resp.data == b'{"birthday":"03/05/1992, 00:00:00","gender":"m","user_id":42,"username":"usernameMock"}\n'
    assert resp.status_code == 200


def test_api_get_user_snapshots(api_flask_client):
    resp = api_flask_client.get('http://127.0.0.1:5000/users/42/snapshots')
    assert resp.data == b'1575446887339'
    assert resp.status_code == 200


def test_api_get_user_snapshot_results(api_flask_client):
    resp = api_flask_client.get('http://127.0.0.1:5000/users/42/snapshots/1575446887339')
    assert resp.data == b'{"results":["pose","depth_image","feelings","color_image"],"snapshot_id":"1575446887339"}\n'
    assert resp.status_code == 200


@pytest.mark.skip(reason="The paths strings inside changes with every run, so it's a good manual check if you need it")
def test_api_get_user_snapshot_result_specific(api_flask_client):
    resp = api_flask_client.get('http://127.0.0.1:5000/users/42/snapshots/1575446887339/color_image')
    assert resp.data == b'{"color_image_path":"/home/user/work/brainComputer/tests/data/snapshots/42_Dan Gittik/1575446887339/color_image.png","data_path":"/home/user/work/brainComputer/tests/data/snapshots/42_Dan Gittik/1575446887339/color_data","height":1080,"width":1920}\n'
    assert resp.status_code == 200
