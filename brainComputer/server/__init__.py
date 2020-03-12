import threading

from brainComputer.utils.listener import Listener
from brainComputer.utils.protocol import Config, User, Snapshot
from .utils import rabbitmq_publish_snapshots


def run_server(host: str, port: int, publish):
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
        """ Handle the connection and then print to stdout
        :return:
        """
        try:
            # conf = Config(CONF_FIELDS)
            with self.connection as con:
                user = User.deserialize(con.receive())
                con.send(conf.serialize())
                snap_bytes = con.receive()
                snap = Snapshot.deserialize(snap_bytes, CONF_FIELDS)

        # TODO: publish to queue. with rabbitmq_publish_snapshots() and Pika or something?

        except Exception as e:
            print(f"Abort connection to failed client. {e}")
