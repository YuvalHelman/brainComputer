import socket
import time
import struct
import click


@click.command(name='upload')
@click.option('--address', '-a', default='127.0.0.1:5000', help="address of the server")
@click.option('--user', '-u', help='user ID.')
@click.option('--thought', '-t', help='an arbitrary string to send to the server.')
def upload_thought(address, user, thought):
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


if __name__ == '__main__':
    pass
