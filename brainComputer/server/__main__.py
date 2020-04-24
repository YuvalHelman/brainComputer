import brainComputer.utils.rabbit_utils as rabmq
import brainComputer
import click
import pika
import furl
from . import run_server


@click.group()
def cli():
    pass


@cli.command(name='run-server')
@click.option('--host', '-h', default='127.0.0.1', help="address of the server")
@click.option('--port', '-p', default='8000', type=int, help='port of the server')
@click.option('--data_path', '-d', default=brainComputer.ROOT_DIR + "data/", help="path on disk to save big data")
@click.argument('publish_url')
def run_server_cli(host, port, data_path, publish_url):
    """ accept connections from clients, receive the uploaded samples and sends them to the message queue.
    :param host: Network IP Address or Hostname to connect to.
    :param port: Network Port to bind.
    :param data_path: a path to save data that needs to be saved on the disk.
    :param publish_url: message queue url to publish data to upon receiving uploaded samples.
    """
    publisher_url = furl.furl(publish_url)

    def publish(message):
        try:
            con = pika.BlockingConnection(pika.ConnectionParameters(publisher_url.host, publisher_url.port))
            if publisher_url.scheme == 'rabbitmq':
                rabmq.publish_fanout(connection=con, exchange_name=rabmq.SNAPSHOT_EXCHANGE, data=message)
            con.close()
        except Exception as e:
            print(f"publish from server to queue failed: {e}")

    run_server(host, port, data_path, publish)


if __name__ == '__main__':
    cli()
