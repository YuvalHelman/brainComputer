from .connection import Connection
import socket


class Listener:
    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr

        self.serversocket = None

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def __repr__(self):
        return f'Listener(port={self.port!r}, host={self.host!r}, backlog={self.backlog!r}, reuseaddr={self.reuseaddr!r})'

    #  start() method, which starts listening,
    #  and a stop() method, which stops listening and closes the socket.
    def start(self):
        """ which starts listening """
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create an INET, STREAMing socket
        serversocket.bind((self.host, self.port))  # bind the socket to a public host, and a well-known port
        serversocket.listen(self.backlog)  # start listening for connections

        self.serversocket = serversocket

    def stop(self):
        """ stops listening and closes the socket """
        self.serversocket.close()

    def accept(self):
        """ which waits for a connection, accepts it, and returns a Connection object. """
        try:
            clientsocket, address = self.serversocket.accept()
            return Connection(clientsocket)
        except Exception as e:
            print('Exception accepting or handling first half of message from client:', e)
            return 1
