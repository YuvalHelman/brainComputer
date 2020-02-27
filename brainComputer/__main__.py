import click
from .web import run_webserver
from .utils.readers import ReaderBinary, ReaderProtobuf


@click.group()
def cli():
    pass


# @cli.command(name='run')
# @click.option('--host', '-h', default='127.0.0.1', help="address of the server")
# @click.option('--port', '-p', default='5000', help='port of the server')
# @click.argument('publish')
# def run_server_cli(address, port, publish):
#     try:
#         port = int(port)
#     except ValueError:
#         print('port argument is not valid.')
#         return
#
#     run_server(address, port, publish)  # TODO: add publish
#

# cli.add_command(run_server_cli)


# @cli.command(name='upload')
# @click.option('--address', '-a', default='127.0.0.1:5000', help="address of the server")
# @click.option('--data_path', '-d', default='dataFiles/sample.mind.gz', help='the file which fetches the data.')
# @click.option('--version', '-v', default='2', help='version of reader to use. there are v1 and v2 at the moment')
# def upload_thought_cli(address, data_path, version='2'):
#     upload_thought(address, data_path, version)


# cli.add_command(upload_thought_cli)


@cli.command(name='read')
@click.option('--version', '-v', default='2', help='version of reader to use. there are v1 and v2 at the moment')
@click.option('--data_path', '-d', default='dataFiles/sample.mind.gz', help="path to the data file to read from")
def read_messages_to_cli(version='2', data_path='dataFiles/sample.mind.gz'):
    if version == '2':
        r = ReaderProtobuf(data_path)
    elif version == '1':
        r = ReaderBinary(data_path)  # This uses a different kind of data file!
    else:
        print("Choose between version 1 or 2")
        return
    print(r.user)
    for snap in r:
        print(snap)
        print("Click any button to continue presenting snapshots...")
        txt = input()


# cli.add_command(read_messages_to_cli)
# cli.add_command(run_webserver)


if __name__ == '__main__':
    cli()
