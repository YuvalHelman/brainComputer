import click
from .utils.readers import ReaderBinary, ReaderProtobuf
from .utils.connection import Connection
from .utils.protocol import Hello, Config


def upload_thought(address, data_path, version):
    ip, port = address.split(":")
    try:
        if version == '2':
            reader = ReaderProtobuf(data_path)
        else:
            reader = ReaderBinary(data_path)
        hello = Hello(reader.user)
        for snapshot in reader:
            with Connection.connect(host=ip, port=int(port)) as con:
                con.send(hello.serialize())
                conf = Config.deserialize(con.receive())
                snap = snapshot.serialize(conf.fields)
                con.send(snap)
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    pass
