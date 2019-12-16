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
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()

    @classmethod
    @contextlib.contextmanager
    def connect(cls, host, port):
        connection = None
        try:
            sock = socket.socket()
            sock.connect((host, port))
            connection = Connection(sock)
            yield connection
        finally:
            pass

    def send(self, data):
        self.socket.sendall(data)

    def receive_size(self, expected_message_size):
        """ receives as many bytes as were specified by size, or throws an exception if
        the connection was closed before all the data was received. """
        bytes_lst = []
        receivedSize = 0
        while True:
            current_bytes_received = self.socket.recv(expected_message_size)
            curr_bytes_len = len(current_bytes_received)
            if curr_bytes_len == 0:
                raise Exception
            bytes_lst.append(current_bytes_received)
            receivedSize += curr_bytes_len
            if receivedSize >= expected_message_size:
                break
            expected_message_size -= curr_bytes_len
        #  Extract certain bytes from the message:
        messageInBytes = b"".join(bytes_lst)
        return messageInBytes

    def receive(self, expected_message_size):
        """ receives as many bytes as were specified by size, or throws an exception if
        the connection was closed before all the data was received.
        This function now receives a uint32 indicating the length of the message to be sent"""
        MESSAGE_PREFIX_LEN = 4
        msg_len_bytes = self.socket.recv(MESSAGE_PREFIX_LEN)
        msg_len = struct.unpack('I', msg_len_bytes)[0]
        return self.receive_size(msg_len)

    def close(self):
        self.socket.close()


if __name__ == '__main__':
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create an INET, STREAMing socket
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('127.0.0.1', 5000))

    print(f"{serversocket.getsockname()!r}")
    # print(t1)
