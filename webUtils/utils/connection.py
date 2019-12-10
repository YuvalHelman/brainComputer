import socket


class Connection:
    def __init__(self, socket_obj: socket.socket):
        self.socket = socket_obj

    def __repr__(self):
        my_address = self.socket.getsockname()
        dest_address = self.socket.getpeername()
        return f'<Connection from {my_address[0]}:{my_address[1]} to ' \
               f'{dest_address[0]}:{dest_address[1]}>'

    def send(self, data):
        self.socket.sendall(data)

    def receive(self, expected_message_size):
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

    def close(self):
        self.socket.close()


if __name__ == '__main__':
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create an INET, STREAMing socket
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('127.0.0.1', 5000))

    print(f"{serversocket.getsockname()!r}")
    # print(t1)