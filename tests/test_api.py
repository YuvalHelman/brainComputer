import requests


def test_api_getters(api_flask_client):
    resp = api_flask_client.get('http://127.0.0.1:5000/users')
    assert resp.data == b'{"42":"Dan Gittik","43":"Yuval Helman","44":"Yael Livne"}\n'
    assert resp.status_code == 200