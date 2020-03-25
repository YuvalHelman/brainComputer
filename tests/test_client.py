import pytest

from brainComputer.client import upload_sample
from brainComputer.utils.brain_pb2 import User as PbUser
import threading


class mockedProtoReader:
    def __init__(self, file):
        """ Return a PbUser object"""
        self.file = file
        protoObj = PbUser()
        protoObj.ParseFromString(b'\x08*\x12\nDan Gittik\x18\xe0\x90\xd5\xcd\x02')
        self.user = protoObj

    def __next__(self):
        raise StopIteration()


def test_upload_sample(monkeypatch, capsys):
    from brainComputer.utils.readers import ReaderProtobuf

    monkeypatch.setattr(ReaderProtobuf, "__init__", value=mockedProtoReader.__init__)
    monkeypatch.setattr(ReaderProtobuf, "__next__", value=mockedProtoReader.__next__)

    serv = threading.Thread(target=run_fake_server, args=('127.0.0.1', 8888))
    serv.daemon = True
    serv.start()
    upload_sample('127.0.0.1', 8888, '/tmp/')

    captured = capsys.readouterr()
    assert "completed sending all snapshots" in captured.out


def run_fake_server(host: str, port: int):
    # Run a server to listen for a connection and then close it
    import socket
    server_sock = socket.socket()
    server_sock.bind((host, port))
    server_sock.listen(0)
    server_sock.accept()
    server_sock.close()
