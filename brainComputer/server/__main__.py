import brainComputer.utils.rabbitmq as rabmq
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
@click.option('--data_path', '-d', default='/tmp/brainComputer/', help="path on disk to save big data")
@click.argument('publish_url')
def run_server_cli(host, port, data_path, publish_url):
    publisher_url = furl.furl(publish_url)

    def publish(message):
        try:
            con = pika.BlockingConnection(pika.ConnectionParameters(publisher_url.host, publisher_url.port))
            if publish_url.scheme == 'rabbitmq':
                rabmq.publish_fanout(connection=con, exchange_name=rabmq.SNAPSHOT_EXCHANGE, data=message)
            con.close()
        except Exception as e:
            print(f"publish from server to queue failed: {e}")

    run_server(host, port, data_path, publish)


if __name__ == '__main__':
    cli()
