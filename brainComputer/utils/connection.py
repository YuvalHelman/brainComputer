import socket
import contextlib
import struct


class Connection:
    """ The Connection object receives a socket and initiates connections to it with the methods:
    connect(), send(), receive()
    """

    def __init__(self, socket_obj: socket.socket):
        self.socket = socket_obj

    def __repr__(self):
        my_address = self.socket.getsockname()
        dest_address = self.socket.getpeername()
        return f'<Connection from {my_address[0]}:{my_address[1]} to ' \
               f'{dest_address[0]}:{dest_address[1]}>'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()

    @classmethod
    @contextlib.contextmanager
    def connect(cls, host: str, port: int):
        connection = None
        try:
            sock = socket.socket()
            sock.connect((host, port))
            connection = Connection(sock)
            yield connection
        finally:
            pass

    def send(self, data):
        msg_len = struct.pack('I', len(data))
        self.socket.sendall(msg_len)
        self.socket.sendall(data)

    def receive_size(self, size):
        """ receives as many bytes as were specified by size, or throws an exception if
        the connection was closed before all the data was received. """
        expected_msg_size = size
        bytes_lst = []
        receivedSize = 0
        while True:
            data = self.socket.recv(expected_msg_size)
            if not data or len(data) == 0:
                break
            bytes_lst.append(data)
            receivedSize += len(data)
            expected_msg_size -= len(data)
        if expected_msg_size > 0:
            raise Exception("Receive failed")
        messageInBytes = b"".join(bytes_lst)
        return messageInBytes

    def receive(self):
        """ receives a uint32 indicating the length of the message to be sent and recieves that amount of bytes """
        try:
            msg_len_bytes = self.socket.recv(4)
            msg_len, *_ = struct.unpack('I', msg_len_bytes)
            return self.receive_size(msg_len)
        except Exception as e:
            print(f"receive failed: {e}")

    def close(self):
        self.socket.close()
