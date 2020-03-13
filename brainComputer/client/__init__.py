from brainComputer.utils.readers import ReaderBinary, ReaderProtobuf
from brainComputer.utils.connection import Connection
from brainComputer.client.utils import convert_to_protocol_user, convert_to_protocol_snapshot


def upload_sample(host: str, port: int, path: str):
    """ """
    try:
        reader = ReaderProtobuf(path)
        pb_user = convert_to_protocol_user(reader.user)
        for snapshot in reader:
            pb_snap = convert_to_protocol_snapshot(snapshot)
            with Connection.connect(host, port) as con:
                con.send(pb_user.SerializeToString())
                con.send(pb_snap.SerializeToString())
    except Exception as e:
        print(f'ERROR: {e}')


if __name__ == '__main__':
    upload_sample('127.0.0.1', 8000, '/home/user/Downloads/sample.mind.gz')
