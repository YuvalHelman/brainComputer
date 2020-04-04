import click
import furl

from . import run_api_server


@click.group()
def cli():
    pass


@cli.command(name='save')
@click.option('--host', '-h', default='127.0.0.1', help="url of the database")
@click.option('--port', '-p', default='5000', help="url of the database")
@click.option('--database', '-d', default='mongodb://127.0.0.1:27017', help="url of the database")
def save_cli(database, topic_name, data_path):
    """  accepts a parser name and a path to some raw data and prints the result.
         This way of invocation runs the parser exactly once """
    with open(data_path, 'r') as f:
        data = f.read()

    # s = Saver(database)
    # s.save(topic_name, data)


if __name__ == "__main__":
    cli()
