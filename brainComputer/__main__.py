import click
from .client import upload_thought
from .server import run_server
from .web import run_webserver
from .utils.reader import read_messages_to_cli


@click.group(name="brain")
def cli():
    pass


cli.add_command(run_webserver)
cli.add_command(read_messages_to_cli)


@click.group(name="client")
def client_cli():
    pass


client_cli.add_command(upload_thought)


@click.group(name="server")
def server_cli():
    pass


server_cli.add_command(run_server)


if __name__ == '__main__':
    cli()
