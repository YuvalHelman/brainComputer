import click
from .utils.reader import ReaderBinary
from .utils.connection import Connection
from .utils.protocol import Hello, Config


@click.command(name='upload')
@click.option('--address', '-a', default='127.0.0.1:5000', help="address of the server")
@click.option('--data_path', '-d', help='the file which fetches the data.')
def upload_thought(address, data_path):
    ip, port = address.split(":")
    try:
        reader = ReaderBinary(data_path)
        hello = Hello(reader.user)
        for snapshot in reader:
            with Connection.connect(host=ip, port=int(port)) as con:
                con.send(hello.serialize())
                conf = Config.deserialize(con.receive())
                con.send(snapshot.serialize(conf.fields_list))
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    pass
