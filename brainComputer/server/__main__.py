from . import run_server
from .utils import rabbitmq_publish_snapshots
import click
import pika
from furl import furl


@click.group()
def cli():
    pass


@cli.command(name='run-server')
@click.option('--host', '-h', default='127.0.0.1', help="address of the server")
@click.option('--port', '-p', default='8000', type=int, help='port of the server')
@click.argument('publish_url')
def run_server_cli(host, port, publish_url):
    publisher_url = furl(publish_url)

    def publish(message):
        con = pika.BlockingConnection(pika.ConnectionParameters(publisher_url.host, publisher_url.port))
        if publish_url.scheme == 'rabbitmq':
            rabbitmq_publish_snapshots(connection=con, message=message)

    run_server(host, port, publish)


if __name__ == '__main__':
    cli()
