import threading
import time
import random

from brainComputer.server import run_server


def dummy_client(host: str, port: int, user_data, snap_data):
    from brainComputer.utils.connection import Connection
    with Connection.connect(host, port) as con:
        con.send(user_data)
        con.send(snap_data)


def test_run_server(capsys, monkeypatch, encoded_snapshot_user_json_no_data, test_data_path, pb_protocol_user_data,
                    pb_protocol_snapshot_data):
    host = '127.0.0.1'
    port = random.randint(6000, 10000)
    serv = threading.Thread(target=run_server, args=(host, port,
                                                     test_data_path + 'snapshots/', print))
    serv.daemon = True
    serv.start()
    time.sleep(0.1)  # let server go up
    dummy_client(host, port, pb_protocol_user_data, pb_protocol_snapshot_data)
    time.sleep(0.1)  # let server compute output
    captured = capsys.readouterr()
    l = captured.out.split('\n')
    assert encoded_snapshot_user_json_no_data in captured.out
