import threading
import json

import brainComputer
from brainComputer.utils.listener import Listener
from brainComputer.utils.brain_pb2 import User as PbUser
from brainComputer.utils.brain_pb2 import Snapshot as PbSnapshot
from brainComputer.utils.protocol import user_snap_pb_to_json


def run_server(host: str, port: int, data_path=brainComputer.RESULTS_DIR, publish=print):
    print(f"## listening on {host}:{port} and passing received messages to publish ##")
    with Listener(host, port) as listener:
        while True:
            con = listener.accept()
            handler = ConnectionHandler(con, publish, data_path)
            handler.start()


class ConnectionHandler(threading.Thread):
    def __init__(self, connection, publish, data_path):
        super().__init__()
        self.connection = connection
        self.publish = publish
        self.data_path = data_path

    def run(self):
        """ Handle the connection
        :return:
        """
        try:
            with self.connection as con:
                pb_user = PbUser()
                pb_snapshot = PbSnapshot()
                pb_user.ParseFromString(con.receive())
                pb_snapshot.ParseFromString(con.receive())
            self.publish(user_snap_pb_to_json(pb_user, pb_snapshot, self.data_path))
            # print(user_snap_pb_to_json(pb_user, pb_snapshot, self.data_path))  # DEBUG
        except Exception as e:
            print(f"Abort connection to failed client. {e}")
            raise e  # DEBUG


if __name__ == '__main__':
    run_server('127.0.0.1', 8000)
