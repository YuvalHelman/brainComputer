import datetime
import socket
import threading
import struct
import pillow
from pathlib import Path
import click
import json
from .utils.listener import Listener
from .utils.protocol import Hello, Config, Snapshot

_GLOBAL_WRITE_LOCK = threading.Lock()


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
    fields = ['translation', 'color_image']

    def __init__(self, connection, data_dir):
        super().__init__()
        self.connection = connection  # a socket of communication with a client
        if data_dir.split("/")[-1] != '':  # the path doesn't have an ending "/"
            self.data_dir = data_dir + "/"

    def run(self):
        """ Handle the connection and then print to stdout
        :return:
        """
        conf = Config(ConnectionHandler.fields)
        with self.connection as con:
            hello = Hello.deserialize(con.receive())
            con.send(conf.serialize())
            snap = Snapshot.deserialize(con.receive(), ConnectionHandler.fields)

        self.write_translation_to_file(hello.user.id, snap.timestamp, snap.translation)


        # returnedTuple = self.receive_unpack(expected_message_size=20, unpack_format_string="<QQI")
        # if returnedTuple is None:
        #     print(f"error: First half of message error.")
        #     self.clientsocket.close()
        #     return 1
        # userID, timeInSec, thoughtSize = returnedTuple
        # #  Handle receiving the rest of the message:
        # clientThought = self.receive_unpack(expected_message_size=thoughtSize,
        #                                     unpack_format_string="<%ds" % thoughtSize)
        # if clientThought is None:
        #     print(f"error: client {userID} didn't send a message of said length.")
        #     self.clientsocket.close()
        #     return 1
        # try:
        #     clientThought = clientThought[0].decode("utf-8")
        #     self.write_thought_to_file(clientThought, userID, timeInSec)
        #     self.clientsocket.close()
        # except Exception as e:
        #     print('Exception:', e)
        #     self.clientsocket.close()

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

    def write_translation_to_file(self, user_id, timestamp, translation):
        """ the server saves the thought into:
        data/user_id/datetime/translation.json
        With the following JSON format: {"x": x, "y": y, "z": z}.
        """
        timeString = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d_%H-%M-%S')
        p_dir = Path(f"{self.data_dir}{user_id}/{timeString}")

        if not p_dir.exists():
            p_dir.mkdir(parents=True, exist_ok=True)

        p = Path(f"{p_dir}/translation.json")

        with _GLOBAL_WRITE_LOCK:  # Lock before writing
            with p.open(mode="w") as fd:
                fd.write(json.dumps({"x": 0, "y": 0, "z": 0}))

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
