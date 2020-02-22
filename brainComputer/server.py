from .utils.listener import Listener
from .utils.protocol import Hello, Config, Snapshot
from .utils.parser import Parsers, ParserContext
import json
import threading
import click
from flask import Flask, request

CONF_FIELDS = ['translation', 'color_image']


@click.group()
def cli():
    pass


@cli.command(name='run-server')
@click.option('--host', '-h', default='127.0.0.1', help="address of the server")
@click.option('--port', '-p', default='8000', help='port of the server')
@click.argument('publish')
def run_server(host, port, publish):
    address = f'{host}:{port}'
    parsers_dict = Parsers.load_modules()
    with Listener(host, port) as listener:
        while True:
            con = listener.accept()
            handler = ConnectionHandler(con, parsers_dict)
            handler.start()  # start() invokes .run()


class ConnectionHandler(threading.Thread):
    def __init__(self, connection, parsers):
        super().__init__()
        self.connection = connection
        self.parsers = parsers
        # self.data_dir = data_dir
        # if data_dir.split("/")[-1] != '':
        #     self.data_dir += "/"

    def run(self):
        """ Handle the connection and then print to stdout
        :return:
        """
        conf = Config(CONF_FIELDS)

        with self.connection as con:
            hello = Hello.deserialize(con.receive())
            con.send(conf.serialize())
            # import pdb; pdb.set_trace()  # DEBUG
            snap_bytes = con.receive()
            snap = Snapshot.deserialize(snap_bytes, CONF_FIELDS)

        # parse_context = ParserContext(self.data_dir, hello, snap)
        # for field_name, func_handler in self.parsers.items():
        #     if field_name in CONF_FIELDS:
        #         func_handler(parse_context, snap)


if __name__ == '__main__':
    cli()
