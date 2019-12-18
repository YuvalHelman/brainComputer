import datetime
import socket
import threading
import struct
from PIL import Image
from pathlib import Path
import click
import json
from .utils.listener import Listener
from .utils.protocol import Hello, Config, Snapshot
from .utils.parser import Parser

_GLOBAL_WRITE_LOCK = threading.Lock()
CONF_FIELDS = ['translation', 'color_image']


@click.command(name='run')
@click.option('--address', '-a', default='127.0.0.1:5000', help="address of the server")
@click.option('--data_dir', '-d', help='The directory where the server fetches data.')
def run_server(address, data_dir):  # python -m server run -a "127.0.0.1:5000" -d data/
    ip, port = address.split(":")
    with Listener(ip, port) as listener:
        while True:
            con = listener.accept()
            handler = ConnectionHandler(con, str(data_dir))
            handler.start()  # start() invokes .run()


class ConnectionHandler(threading.Thread):

    def __init__(self, connection, data_dir):
        super().__init__()
        self.connection = connection  # The current Connection Object with the client
        self.data_dir = data_dir
        if data_dir.split("/")[-1] != '':  # always have a postfix '/' in the path
            self.data_dir += "/"

    def run(self):
        """ Handle the connection and then print to stdout
        :return:
        """
        conf = Config(CONF_FIELDS)
        with self.connection as con:
            hello = Hello.deserialize(con.receive())
            con.send(conf.serialize())
            snap = Snapshot.deserialize(con.receive(), CONF_FIELDS)

        context_parser = Parser(self.data_dir, hello, snap)
        for func_name, func in context_parser.fields_dict.items():
            if func_name in CONF_FIELDS:
                func(context_parser, snap)

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

    def write_thought_to_file_old(self, thought, userID, timeInSec):
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


if __name__ == '__main__':
    pass
