import click
from .utils.readers import ReaderBinary, ReaderProtobuf
from .utils.connection import Connection
from .utils.protocol import Hello, Config
import requests
import json


@click.group()
def cli():
    pass


@cli.command(name='upload-sample')
@click.option('--host', '-h', default='127.0.0.1', help="address of the server")
@click.option('--port', '-p', default='8000', help='port of the server')
@click.argument('path')
def upload_sample(host, port, path='dataFiles/sample.mind.gz'):
    try:
        port = int(port)
    except ValueError as e:
        print(f'bad port argument: {e}')
        return 1

    try:
        reader = ReaderProtobuf(path)
        hello = Hello(reader.user)
        for snapshot in reader:
            # import pdb;pdb.set_trace()  # DEBUG
            with Connection.connect(host, port) as con:
                con.send(hello.serialize())
                conf = Config.deserialize(con.receive())
                snap = snapshot.serialize(conf.fields)

                con.send(snap)
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


# r = sess.post(f"http://{address}/config", json=json_user_info)
# config_list = json.loads(r.content)
# import pdb; pdb.set_trace()
# snap_json = snapshot.serialize(config_list)
#
# r = sess.post(f"http://{address}/snapshot", data=snap_json, )


if __name__ == '__main__':
    cli()
