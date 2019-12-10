import click
from .client import upload_thought
from .server import run

@click.group()
def cli():
    pass


cli.add_command(upload_thought)
cli.add_command(run)


if __name__ == '__main__':
    cli()
