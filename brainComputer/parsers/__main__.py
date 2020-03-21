import click

import brainComputer.utils.rabbitmq as rabmq
from . import run_parser
from .utils import get_parser_function


@click.group()
def cli():
    pass


@cli.command(name='parse')
@click.argument('parser_name')
@click.argument('data')
def parse_cli(parser_name, data):
    """  accepts a parser name and a path to some raw data and prints the result.
         This way of invocation runs the parser exactly once """
    run_parser(parser_name, data)


@cli.command(name='run-parser')
@click.argument('parser_name')
@click.argument('mq_url')
def run_parser_cli(parser_name, publish_url):
    """ running the parser as a service, which works with a message queue indefinitely """
    try:
        parser_func = get_parser_function(parser_name)
    except KeyError:
        print(f"{parser_name} isn't a valid parser name")
        return 1

    if publish_url.scheme == 'rabbitmq':
        rabmq.consume_retrieve(rabmq_url=publish_url, consume_exchange_name=rabmq.SNAPSHOT_EXCHANGE,
                               publish_exchange_name=parser_name, pre_publish_func=parser_func)


if __name__ == "__main__":
    cli()
