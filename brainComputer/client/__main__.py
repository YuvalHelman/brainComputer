import click
from . import upload_sample


@click.group()
def cli():
    pass


@cli.command(name='upload-sample')
@click.option('-h', '--host', default='127.0.0.1', help="address of the server")
@click.option('-p', '--port', default='8000', type=int, help='port of the server')
@click.argument('path')
def upload_sample_cli(host, port, path):
    upload_sample(host, port, path)


if __name__ == "__main__":
    cli()
