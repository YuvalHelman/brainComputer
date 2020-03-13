import threading
from brainComputer.utils.listener import Listener
from brainComputer.utils.brain_pb2 import User as PbUser
from brainComputer.utils.brain_pb2 import Snapshot as PbSnapshot
from brainComputer.server.utils import rabbitmq_publish_snapshots


def run_server(host: str, port: int, publish=print):
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

        # TODO: publish to queue. with rabbitmq_publish_snapshots() and Pika or something?

        except Exception as e:
            print(f"Abort connection to failed client. {e}")


if __name__ == '__main__':
    print("go")  # DEBUG
    run_server('127.0.0.1', 8000)
