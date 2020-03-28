import pytest
import threading
import time
import random

import tests
from brainComputer.server import run_server


def dummy_client(host: str, port: int):
    from brainComputer.utils.connection import Connection
    with Connection.connect(host, port) as con:
        con.send(b'\x08*\x12\nDan Gittik\x18\xe0\x90\xd5\xcd\x02')
        con.send(
            b'\x08\xab\xf7\xce\xff\xec-\x12C\n\x1b\t\x00\x00\x00 N1\xdf?\x11\x00\x00\x00\xe0k\n}?\x19\x00\x00\x00\xa0\xfd\x16\xf2\xbf\x12$\t\xd5yw\xc0\x00\xe0\xbb\xbf\x11\x1deI\xc0\xb3\x1f\xd1\xbf\x19\xdf[]\xa0\x18\xc8\x95\xbf!\xd1F\x83\xa0\xd4\xa0\xee?\x1a\x00"\x00*\x00')


def test_run_server(capsys, monkeypatch, encoded_snapshot_user_json_no_data, test_data_path):
    host = '127.0.0.1'
    port = random.randint(6000, 10000)
    serv = threading.Thread(target=run_server, args=(host, port,
                                                     test_data_path + 'snapshots/', print))
    serv.daemon = True
    serv.start()
    time.sleep(0.1)  # let server go up
    dummy_client(host, port)
    time.sleep(0.1)  # let server compute output
    captured = capsys.readouterr()
    l = captured.out.split('\n')
    assert encoded_snapshot_user_json_no_data in captured.out
