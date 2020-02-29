import click
from .binaryReader import ReaderBinary
from .protoReader import ReaderProtobuf


@click.group()
def cli():
    pass


@cli.command(name='read')
@click.option('--version', '-v', default='2', help='versions available: {1, 2}')
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


if __name__ == "__main__":
    cli()
