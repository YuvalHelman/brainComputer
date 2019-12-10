import socket
import sys
import time
from sys import getsizeof
import struct
import click


@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def upload_thought(address, user, thought):
    """
    :param address: str.  example: 127.0.0.1:5000
    :param user: str example: 1
    :param thought: arbitrary string.
    :return:
    """
    ip, port = address.split(":")
    thought_encoded = thought.encode("utf-8")
    thought_size = len(thought)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to Server
        s.connect((ip, int(port)))
        # wrap the data and send to server
        s.sendall(struct.pack("<QQI%ds" % thought_size, int(user), int(time.time()), thought_size, thought_encoded))
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


def main(argv):
    cli.main()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
