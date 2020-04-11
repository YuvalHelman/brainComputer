from brainComputer.api import run_api_server

import requests


def test_api_getters(api_flask_client):
    rv = api_flask_client.get('http://127.0.0.1:5000/users')
    print(rv.data)
