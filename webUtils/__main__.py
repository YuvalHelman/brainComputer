import click
from .client import upload_thought
from .server import run
from .web import run_webserver

@click.group()
def cli():
    pass


cli.add_command(upload_thought)
cli.add_command(run)
cli.add_command(run_webserver)


if __name__ == '__main__':
    cli()
