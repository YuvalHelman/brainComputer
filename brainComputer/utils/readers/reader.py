from .protoReader import ReaderProtobuf
from .binaryReader import ReaderBinary
import click


@click.command(name='read')
@click.option('--version', '-v', default='2', help='version of reader to use. there are v1 and v2 at the moment')
@click.option('--data_path', '-d', default='dataFiles/sample.mind.gz', help="path to the data file to read from")
def read_messages_to_cli(version='v2', data_path='dataFiles/sample.mind.gz'):
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
        txt = input()
