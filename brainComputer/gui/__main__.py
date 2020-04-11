import click

from . import run_server


@click.group()
def cli():
    pass


@cli.command(name='run-server')
@click.option('--host', '-h', default='127.0.0.1', help="url of the server")
@click.option('--port', '-p', default='8080', help="url of the server")
@click.option('--database', '-d', default='mongodb://127.0.0.1:27017', help="url of the database")
def run_gui_server_cli(host, port, database):
    run_server(host, port, database)


if __name__ == "__main__":
    cli()
