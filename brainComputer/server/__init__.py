import threading

from brainComputer.utils.listener import Listener
from brainComputer.utils.protocol import Config, Hello, Snapshot

CONF_FIELDS = ['pose']


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
            conf = Config(CONF_FIELDS)
            with self.connection as con:
                hello = Hello.deserialize(con.receive())
                con.send(conf.serialize())
                snap_bytes = con.receive()
                snap = Snapshot.deserialize(snap_bytes, CONF_FIELDS)

        except Exception as e:
            print(f"Abort connection to failed client. {e}")
