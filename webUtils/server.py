import datetime
import socket
import threading
import sys
import struct
from pathlib import Path
from cli import CommandLineInterface

_GLOBAL_WRITE_LOCK = threading.Lock()


def create_server_socket(ip: str, port: str):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create an INET, STREAMing socket
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((ip, int(port)))  # bind the socket to a public host, and a well-known port
    serversocket.listen(1000)  # start listening for connections

    return serversocket


cli = CommandLineInterface()


@cli.command
def run(address, data):  # python server.py run address="127.0.0.1:5000" data=data/
    """
    :param address:
    :param data_dir:
    :return:
    """
    ip, port = address.split(":")
    try:
        serversocket = create_server_socket(ip, port)
    except socket.error as e:
        print(f'Error - Bind failed. Message {e}')
        return 1
    except Exception as e:
        print(e)
        print("creating server socket failed")
        return 1
    while True:  # Iterate different Clients
        try:
            clientsocket, address = serversocket.accept()
            handler = ConnectionHandler(clientsocket, str(data))
            handler.start()  # start invokes .run()
        except Exception as e:
            print('Exception accepting or handling first half of message from client:', e)
            return 1


class ConnectionHandler(threading.Thread):
    def __init__(self, clientsocket, data_dir):
        super().__init__()
        self.clientsocket = clientsocket  # a socket of communication with a client
        self.data_dir = data_dir

    def run(self):
        """ Handle the connection and then print to stdout
        :return:
        """
        returnedTuple = self.receive_unpack(expected_message_size=20, unpack_format_string="<QQI")
        if returnedTuple is None:
            print(f"error: First half of message error.")
            self.clientsocket.close()
            return 1
        userID, timeInSec, thoughtSize = returnedTuple
        #  Handle receiving the rest of the message:
        clientThought = self.receive_unpack(expected_message_size=thoughtSize,
                                            unpack_format_string="<%ds" % thoughtSize)
        if clientThought is None:
            print(f"error: client {userID} didn't send a message of said length.")
            self.clientsocket.close()
            return 1
        try:
            clientThought = clientThought[0].decode("utf-8")
            self.write_thought_to_file(clientThought, userID, timeInSec)
            self.clientsocket.close()
        except Exception as e:
            print('Exception:', e)
            self.clientsocket.close()

    def receive_unpack(self, expected_message_size, unpack_format_string):
        """
        :param expected_message_size: size of the message to get from the socket.
        :param unpack_format_string: format string argument for struct.unpack()
        :return: A tuple of the parts that was unpacked.
        """
        bytes_lst = []
        receivedSize = 0
        leftToReceive = expected_message_size  # == 20 when called first
        try:
            while True:
                current_bytes_received = self.clientsocket.recv(leftToReceive)
                curr_bytes_len = len(current_bytes_received)
                if curr_bytes_len == 0:
                    raise Exception
                bytes_lst.append(current_bytes_received)
                receivedSize += curr_bytes_len
                if receivedSize >= expected_message_size:
                    break
                leftToReceive -= curr_bytes_len
            #  Extract certain bytes from the message:
            messageInBytes = b"".join(bytes_lst)
            return struct.unpack(unpack_format_string, messageInBytes)
        except Exception as e:
            print("recv or unpack failed: ", e)
            return None

    def write_thought_to_file(self, thought, userID, timeInSec):
        timeString = datetime.datetime.fromtimestamp(timeInSec).strftime('%Y-%m-%d_%H-%M-%S')

        if self.data_dir.split("/")[-1] == '':  # the path as an ending "/"
            p_dir = Path(f"{self.data_dir}{userID}/")
            p = Path(f"{self.data_dir}{userID}/{timeString}.txt")
        else:
            p_dir = Path(f"{self.data_dir}/{userID}/")
            p = Path(f"{self.data_dir}/{userID}/{timeString}.txt")
        if not p_dir.exists():
            p_dir.mkdir(parents=True, exist_ok=True)

        with _GLOBAL_WRITE_LOCK:  # Lock before writing
            if p.exists():
                thought = f"\n{thought}"
            with p.open(mode="a") as fd:
                fd.write(f"{thought}")


def main(argv):
    cli.main()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
