from brainComputer.utils.binaryReader import ReaderProtobuf
from brainComputer.utils.connection import Connection
from brainComputer.client.utils import convert_to_protocol_user, convert_to_protocol_snapshot


def upload_sample(host: str, port: int, file_path: str):
    """ Read data from the hardware's binary format, converts it to the format agreed upon the client-server protocol
        and sends it to the server
    :param host: Network IP Address or Hostname of the server.
    :param port: Network Port of the server
    :param file_path: path of the hardware's file to read the data from before sending to the server
    """
    try:
        reader = ReaderProtobuf(file_path)
        pb_user = convert_to_protocol_user(reader.user)
        for snapshot in reader:
            pb_snap = convert_to_protocol_snapshot(snapshot)
            with Connection.connect(host, port) as con:
                con.send(pb_user.SerializeToString())
                con.send(pb_snap.SerializeToString())
        print("completed sending all snapshots")
    except Exception as e:
        print(f'ERROR: {e}')


if __name__ == '__main__':
    upload_sample('127.0.0.1', 8000, '/home/user/Downloads/sample.mind.gz')
