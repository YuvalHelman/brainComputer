import click
from .utils.reader import ReaderBinary
from .utils.connection import Connection
from .utils.protocol import Hello, Config


@click.command(name='upload')
@click.option('--address', '-a', default='127.0.0.1:5000', help="address of the server")
@click.option('--data_path', '-d', default='dataFiles/sample.mind',help='the file which fetches the data.')
def upload_thought(address, data_path):
    ip, port = address.split(":")
    try:
        reader = ReaderBinary(data_path)
        hello = Hello(reader.user)
        for snapshot in reader:
            with Connection.connect(host=ip, port=int(port)) as con:
                con.send(hello.serialize())
                r = con.receive()
                conf = Config.deserialize(r)
                import pdb; pdb.set_trace()  # DEBUG
                con.send(snapshot.serialize(conf.fields))
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    pass
