import threading
from .utils.listener import Listener
from .utils.protocol import Hello, Config, Snapshot
from .utils.parser import Parsers, ParserContext
import json
from flask import Flask, request

app = Flask(__name__)
_GLOBAL_WRITE_LOCK = threading.Lock()
CONF_FIELDS = ['translation', 'color_image']


def run_server(address, data_dir):
    @app.route('/snapshot', methods=['POST'])
    def snapshot():
        json_snapshot = request.get_json()['snapshot']
        
        snap = Snapshot.from_json(json_snapshot)

        import pdb; pdb.set_trace()
        print(2)

    @app.route('/config', methods=['POST'])
    def send_my_config():
        return json.dumps(CONF_FIELDS)

    app.run()

# def run_server(address, data_dir):  # python -m server run -a "127.0.0.1:5000" -d data/
#     ip, port = address.split(":")
#     parsers_dict = Parsers.load_modules()
#     with Listener(ip, port) as listener:
#         while True:
#             con = listener.accept()
#             handler = ConnectionHandler(con, str(data_dir), parsers_dict)
#             handler.start()  # start() invokes .run()


class ConnectionHandler(threading.Thread):

    def __init__(self, connection, data_dir, parsers):
        super().__init__()
        self.connection = connection
        self.data_dir = data_dir
        self.parsers = parsers
        if data_dir.split("/")[-1] != '':
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

        parse_context = ParserContext(self.data_dir, hello, snap)
        for field_name, func_handler in self.parsers.items():
            if field_name in CONF_FIELDS:
                func_handler(parse_context, snap)


if __name__ == '__main__':
    parsers_dict = Parsers.load_modules()
