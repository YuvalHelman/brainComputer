import click
from . import run_parser


@click.group()
def cli():
    pass


@cli.command(name='parse')
@click.argument('parser_name')
@click.argument('data')
def parse_cli(parser_name, data):
    """  accepts a parser name and a path to some raw data and prints the result.
         This way of invocation runs the parser exactly once """
    pass


@cli.command(name='run-parser')
@click.argument('parser_name')
@click.argument('mq_url')
def run_parser_cli(parser_name, mq_url):
    """ running the parser as a service, which works with a message queue indefinitely """
    pass


if __name__ == "__main__":
    cli()
