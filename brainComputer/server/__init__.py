import threading
import json
from brainComputer.utils import get_saving_path
from brainComputer.utils.listener import Listener
from brainComputer.utils.brain_pb2 import User as PbUser
from brainComputer.utils.brain_pb2 import Snapshot as PbSnapshot
from brainComputer.utils.protocol import pbsnapshot_to_dict, pbuser_to_dict
import brainComputer.utils.rabbitmq as rabmq


def run_server(host: str, port: int, publish=print):
    print(f"## listening on {host}:{port} and passing received messages to publish ##")
    with Listener(host, port) as listener:
        while True:
            con = listener.accept()
            handler = ConnectionHandler(con, publish)
            handler.start()  # start() invokes .run()


class ConnectionHandler(threading.Thread):
    def __init__(self, connection, publish):
        super().__init__()
        self.connection = connection
        self.publish = publish

    def run(self):
        """ Handle the connection
        :return:
        """
        try:
            # conf = Config(CONF_FIELDS)
            with self.connection as con:
                user = PbUser()
                snap = PbSnapshot()
                user.ParseFromString(con.receive())
                snap.ParseFromString(con.receive())

            user_dict = pbuser_to_dict(user)
            s = get_saving_path(user, snap, is_proto=True)
            snap_dict = pbsnapshot_to_dict(snap, s)
            self.publish(json.dumps(dict(user=user_dict, snapshot=snap_dict)))

        except Exception as e:
            print(f"Abort connection to failed client. {e}")


if __name__ == '__main__':
    print("go")  # DEBUG
    run_server('127.0.0.1', 8000)
